"""
DDQ Automation — Google Drive Ingestion
Downloads all supported files from a Google Drive folder and returns text chunks.

Authentication options:
  A) Service Account (recommended for production) — set GOOGLE_SERVICE_ACCOUNT_JSON env var
  B) OAuth2 credentials — set GOOGLE_CREDENTIALS_JSON env var (for personal use)
  C) API Key (read-only, public folders only) — set GOOGLE_API_KEY env var

Usage:
    from core.drive import ingest_drive_folder
    chunks = ingest_drive_folder("1abc123xyz...")   # Google Drive folder ID
"""

import io
import os
import json
import tempfile
from pathlib import Path
from typing import List, Optional

from core.ingestion import Chunk, ingest_folder, EXTRACTORS

# ── Google API imports (optional — fail gracefully if not installed) ───────────
try:
    from googleapiclient.discovery   import build
    from googleapiclient.http        import MediaIoBaseDownload
    from google.oauth2               import service_account
    from google.oauth2.credentials   import Credentials
    from google_auth_oauthlib.flow   import InstalledAppFlow
    from google.auth.transport.requests import Request
    import pickle
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False


# ── MIME type → extension mapping ─────────────────────────────────────────────

MIME_TO_EXT = {
    "application/pdf":                                                    ".pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
    "application/msword":                                                 ".doc",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
    "application/vnd.ms-excel":                                          ".xls",
    "text/plain":                                                         ".txt",
    "text/csv":                                                           ".csv",
    "text/markdown":                                                      ".md",
    # Google Workspace types — export as Office formats
    "application/vnd.google-apps.document":     ".docx",
    "application/vnd.google-apps.spreadsheet":  ".xlsx",
    "application/vnd.google-apps.presentation": ".docx",  # basic export
}

GOOGLE_EXPORT_MIME = {
    "application/vnd.google-apps.document":     "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.google-apps.spreadsheet":  "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.google-apps.presentation": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


# ── Authentication ────────────────────────────────────────────────────────────

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]


def _build_service_account_service():
    """Build Drive service from service account JSON (env var or file path)."""
    sa_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not sa_json:
        raise ValueError("GOOGLE_SERVICE_ACCOUNT_JSON environment variable not set.")

    # Accept either a JSON string or a file path
    if sa_json.strip().startswith("{"):
        info = json.loads(sa_json)
    else:
        with open(sa_json) as f:
            info = json.load(f)

    creds = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
    return build("drive", "v3", credentials=creds)


def _build_oauth_service():
    """Build Drive service via OAuth2 (browser flow, stores token locally)."""
    creds = None
    token_path = os.path.expanduser("~/.btsf_ddq_token.pickle")

    if os.path.exists(token_path):
        with open(token_path, "rb") as f:
            creds = pickle.load(f)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
            if not creds_json:
                raise ValueError(
                    "GOOGLE_CREDENTIALS_JSON environment variable not set.\n"
                    "Download OAuth2 credentials JSON from Google Cloud Console."
                )
            if creds_json.strip().startswith("{"):
                import tempfile, json
                tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
                tmp.write(creds_json); tmp.flush()
                creds_file = tmp.name
            else:
                creds_file = creds_json

            flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_path, "wb") as f:
            pickle.dump(creds, f)

    return build("drive", "v3", credentials=creds)


def _build_api_key_service():
    """Build Drive service using API key (read-only public folders)."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    return build("drive", "v3", developerKey=api_key)


def _get_drive_service():
    """Auto-detect available credentials and build Drive service."""
    if not GOOGLE_AVAILABLE:
        raise ImportError(
            "Google API libraries not installed.\n"
            "Run: pip install google-api-python-client google-auth google-auth-oauthlib"
        )

    if os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON"):
        print("  [Auth] Using service account credentials")
        return _build_service_account_service()
    elif os.getenv("GOOGLE_CREDENTIALS_JSON"):
        print("  [Auth] Using OAuth2 credentials")
        return _build_oauth_service()
    elif os.getenv("GOOGLE_API_KEY"):
        print("  [Auth] Using API key (public folders only)")
        return _build_api_key_service()
    else:
        raise ValueError(
            "No Google credentials found. Set one of:\n"
            "  GOOGLE_SERVICE_ACCOUNT_JSON — service account JSON\n"
            "  GOOGLE_CREDENTIALS_JSON     — OAuth2 client credentials JSON\n"
            "  GOOGLE_API_KEY              — API key (public folders only)"
        )


# ── File listing ──────────────────────────────────────────────────────────────

def _list_folder_files(service, folder_id: str) -> List[dict]:
    """List all files in a Drive folder (non-recursive)."""
    files = []
    page_token = None

    while True:
        query = f"'{folder_id}' in parents and trashed = false"
        resp = service.files().list(
            q=query,
            fields="nextPageToken, files(id, name, mimeType, size)",
            pageSize=100,
            pageToken=page_token,
        ).execute()

        files.extend(resp.get("files", []))
        page_token = resp.get("nextPageToken")
        if not page_token:
            break

    return files


def _list_folder_recursive(service, folder_id: str) -> List[dict]:
    """Recursively list all files in a Drive folder and subfolders."""
    all_files = []
    items = _list_folder_files(service, folder_id)

    for item in items:
        if item["mimeType"] == "application/vnd.google-apps.folder":
            # Recurse into subfolder
            sub_files = _list_folder_recursive(service, item["id"])
            # Prefix filename with folder name for clarity
            for f in sub_files:
                f["name"] = f"{item['name']}/{f['name']}"
            all_files.extend(sub_files)
        else:
            all_files.append(item)

    return all_files


# ── File download ─────────────────────────────────────────────────────────────

def _download_file(service, file_id: str, mime_type: str, filename: str,
                   dest_dir: str) -> Optional[str]:
    """Download a file from Drive to dest_dir. Returns local file path or None."""
    ext = MIME_TO_EXT.get(mime_type)
    if ext is None:
        return None  # Unsupported type

    if not EXTRACTORS.get(ext):
        return None  # No extractor for this type

    safe_name = "".join(c if c.isalnum() or c in "._- /" else "_" for c in filename)
    dest_path = os.path.join(dest_dir, safe_name.replace("/", "__") + ext
                             if not safe_name.endswith(ext) else safe_name)

    try:
        # Google Workspace files need export
        export_mime = GOOGLE_EXPORT_MIME.get(mime_type)
        if export_mime:
            request = service.files().export_media(fileId=file_id, mimeType=export_mime)
        else:
            request = service.files().get_media(fileId=file_id)

        buf = io.BytesIO()
        downloader = MediaIoBaseDownload(buf, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()

        with open(dest_path, "wb") as f:
            f.write(buf.getvalue())

        return dest_path

    except Exception as e:
        print(f"  [WARN] Download failed for {filename}: {e}")
        return None


# ── Public API ────────────────────────────────────────────────────────────────

def ingest_drive_folder(folder_id: str,
                        recursive: bool = True,
                        chunk_size: int = 1200,
                        chunk_overlap: int = 200) -> List[Chunk]:
    """
    Download all supported files from a Google Drive folder and return chunks.

    Args:
        folder_id:    Google Drive folder ID (from the URL: drive.google.com/drive/folders/<ID>)
        recursive:    If True, also process files in subfolders
        chunk_size:   Characters per chunk
        chunk_overlap: Overlap between chunks

    Returns:
        List of Chunk objects (same format as ingest_folder)
    """
    service = _get_drive_service()

    print(f"\n[Drive] Listing files in folder {folder_id}...")
    if recursive:
        files = _list_folder_recursive(service, folder_id)
    else:
        files = _list_folder_files(service, folder_id)

    print(f"[Drive] Found {len(files)} files")

    with tempfile.TemporaryDirectory() as tmpdir:
        downloaded = []
        for f in files:
            mime = f.get("mimeType", "")
            ext  = MIME_TO_EXT.get(mime, "")
            if not ext or not EXTRACTORS.get(ext):
                print(f"  [SKIP] {f['name']} ({mime})")
                continue

            print(f"  [DOWN] {f['name']}")
            local_path = _download_file(service, f["id"], mime, f["name"], tmpdir)
            if local_path:
                downloaded.append(local_path)

        print(f"[Drive] Downloaded {len(downloaded)} files — extracting text...")
        chunks = ingest_folder(tmpdir, chunk_size, chunk_overlap)

    return chunks


def folder_id_from_url(url: str) -> str:
    """Extract folder ID from a Google Drive URL."""
    # Handles both:
    # https://drive.google.com/drive/folders/1abc123
    # https://drive.google.com/drive/u/3/folders/1abc123
    import re
    match = re.search(r"/folders/([a-zA-Z0-9_-]+)", url)
    if match:
        return match.group(1)
    # Accept a bare folder ID (no slashes, reasonable length)
    if len(url) >= 10 and "/" not in url and " " not in url:
        return url
    raise ValueError(f"Could not extract folder ID from: {url}")
