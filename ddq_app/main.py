#!/usr/bin/env python3
"""
DDQ Automation Tool — Main Entry Point v1.1
BTSF | Bitcoin Mining Credit Due Diligence

Usage:
    # Local folder
    python main.py --folder /path/to/data_room --deal "Project Broadstone"

    # Google Drive folder (URL or ID)
    python main.py --drive "https://drive.google.com/drive/folders/1abc..." --deal "Project Broadstone"

    # With schema + Excel output
    python main.py --folder /path/to/data_room --deal "Project Broadstone" --schema --excel

    # Override detected signals manually
    python main.py --folder /path/to/data_room --deal "Project XXX" \
        --signals-override "greenfield=true,hosting=false,existing_debt=true"

Required environment variable:
    ANTHROPIC_API_KEY=sk-ant-your-key-here

Optional (Google Drive only — one of):
    GOOGLE_SERVICE_ACCOUNT_JSON  path or JSON string of service account credentials
    GOOGLE_CREDENTIALS_JSON      path or JSON string of OAuth2 client credentials
    GOOGLE_API_KEY               API key (public folders only)
"""

import argparse
import os
import sys
import time
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))

from config import ANTHROPIC_API_KEY, OUTPUT_DIR
from core.ingestion import ingest_folder
from core.signals   import detect_signals, SIGNALS
from core.questions import assemble_questions, CONDITIONAL_BLOCKS
from core.generator import generate_answers
from core.writer    import export_docx


# ── Banner ────────────────────────────────────────────────────────────────────

def print_banner():
    print("""
╔══════════════════════════════════════════════════════════╗
║        BTSF DDQ Automation Tool — v1.1                  ║
║        Bitcoin Mining Credit Due Diligence               ║
║                                                          ║
║  Upgrades:                                               ║
║    + Google Drive ingestion  (--drive)                   ║
║    + Structured JSON schema  (--schema)                  ║
║    + Excel underwriting seed (--excel)                   ║
║    + Signal overrides        (--signals-override)        ║
╚══════════════════════════════════════════════════════════╝
""")


def validate_env():
    if not ANTHROPIC_API_KEY:
        print("[ERROR] ANTHROPIC_API_KEY environment variable is not set.")
        print("        export ANTHROPIC_API_KEY=sk-ant-...")
        sys.exit(1)


# ── Signal override parser ────────────────────────────────────────────────────

def parse_signals_override(override_str: str) -> dict:
    """
    Parse "greenfield=true,hosting=false,existing_debt=true"
    Returns dict of {signal_key: bool}.
    """
    if not override_str:
        return {}

    overrides = {}
    for part in override_str.split(","):
        part = part.strip()
        if "=" not in part:
            print(f"  [WARN] Skipping malformed override: {part!r}")
            continue
        key, val = part.split("=", 1)
        key = key.strip().lower()
        val = val.strip().lower()

        if key not in SIGNALS:
            print(f"  [WARN] Unknown signal key: {key!r}")
            print(f"         Valid keys: {', '.join(SIGNALS.keys())}")
            continue
        if val not in ("true", "false", "1", "0", "yes", "no"):
            print(f"  [WARN] Invalid value {val!r} for {key} — use true or false")
            continue

        overrides[key] = val in ("true", "1", "yes")

    return overrides


# ── Core pipeline ─────────────────────────────────────────────────────────────

def run_pipeline(
    folder_path:      str  = None,
    drive_url:        str  = None,
    deal_name:        str  = "Project XXX",
    verbose:          bool = True,
    site_info:        dict = None,
    signals_override: dict = None,
    run_schema:       bool = False,
    run_excel:        bool = False,
) -> dict:
    """
    Orchestrates the full DDQ pipeline.
    Returns dict with paths to all generated output files.
    """
    t0 = time.time()
    outputs = {}

    # ── Step 1: Ingest ────────────────────────────────────────────────────────
    print("\n" + "="*60)
    print("STEP 1/4 — Document ingestion")
    print("="*60)

    if drive_url:
        from core.drive import ingest_drive_folder, folder_id_from_url
        folder_id = folder_id_from_url(drive_url)
        print(f"[Drive] Folder ID: {folder_id}")
        chunks = ingest_drive_folder(folder_id)
    elif folder_path:
        chunks = ingest_folder(folder_path)
    else:
        print("[ERROR] Provide either --folder or --drive")
        sys.exit(1)

    if not chunks:
        print("[ERROR] No text could be extracted from the data room.")
        sys.exit(1)

    # ── Step 2: Signal detection + overrides ──────────────────────────────────
    print("\n" + "="*60)
    print("STEP 2/4 — Signal detection")
    print("="*60)

    signals = detect_signals(chunks)

    if signals_override:
        print("\n[Overrides] Applying manual signal overrides:")
        for k, v in signals_override.items():
            old = signals.get(k)
            signals[k] = v
            changed = "→ changed" if old != v else "→ unchanged"
            print(f"  {'✓' if v else '✗'} {k}: {old} → {v}  {changed}")

    # ── Step 3: Question assembly ─────────────────────────────────────────────
    print("\n" + "="*60)
    print("STEP 3/4 — Assembling question set")
    print("="*60)

    questions = assemble_questions(signals)
    section_counts = Counter(q.section for q in questions)

    print(f"[Questions] {len(questions)} total questions assembled")
    active_blocks = [k for k, v in signals.items() if v and k in CONDITIONAL_BLOCKS]
    if active_blocks:
        print(f"[Questions] Conditional blocks activated: {', '.join(active_blocks)}")
    else:
        print("[Questions] No conditional blocks activated — minimum set only")

    print("\n  Section breakdown:")
    for section, count in sorted(section_counts.items()):
        print(f"    {section}: {count}")

    # ── Step 4: Answer generation ─────────────────────────────────────────────
    print("\n" + "="*60)
    print("STEP 4/4 — Generating answers via Claude API")
    print("="*60)

    answers = generate_answers(questions, chunks, verbose=verbose)

    counts = Counter(a.confidence for a in answers)
    print(f"\n[Completion] {len(answers)} questions processed:")
    print(f"  ✓ Answered : {counts.get('answered', 0)}")
    print(f"  ~ Partial  : {counts.get('partial',  0)}")
    print(f"  ✗ Gap      : {counts.get('gap',      0)}")

    # ── Step 5a: DDQ Word document ────────────────────────────────────────────
    print("\n" + "="*60)
    print("OUTPUT 1/3 — DDQ Word document")
    print("="*60)

    ddq_path = export_docx(answers, signals, deal_name, site_info)
    outputs["ddq_docx"] = ddq_path

    # ── Step 5b: Structured JSON schema (optional) ────────────────────────────
    if run_schema or run_excel:
        print("\n" + "="*60)
        print("OUTPUT 2/3 — Structured JSON deal schema")
        print("="*60)

        from core.schema import extract_schema, save_schema_json, print_schema_summary
        schema = extract_schema(answers, deal_name)
        schema_path = save_schema_json(schema, deal_name)
        outputs["schema_json"] = schema_path
        print_schema_summary(schema)
    else:
        schema = None

    # ── Step 5c: Excel underwriting model (optional) ──────────────────────────
    if run_excel:
        print("\n" + "="*60)
        print("OUTPUT 3/3 — Excel underwriting model")
        print("="*60)

        from core.excel import export_excel
        excel_path = export_excel(schema, deal_name)
        outputs["excel"] = excel_path

    # ── Summary ───────────────────────────────────────────────────────────────
    elapsed = time.time() - t0
    print("\n" + "="*60)
    print(f"✓ Complete in {elapsed:.1f}s   |   {len(answers)} questions   |   "
          f"{counts.get('answered',0)} answered / "
          f"{counts.get('partial',0)} partial / "
          f"{counts.get('gap',0)} gap")
    print("="*60)
    print("\nOutput files:")
    labels = {"ddq_docx": "DDQ Word doc", "schema_json": "Deal schema JSON",
              "excel": "Excel underwriting model"}
    for key, path in outputs.items():
        print(f"  [{labels.get(key, key)}]  {path}")

    return outputs


# ── CLI entry point ───────────────────────────────────────────────────────────

def main():
    print_banner()
    validate_env()

    parser = argparse.ArgumentParser(
        description="BTSF DDQ Automation — fills a Bitcoin mining credit DDQ from a data room",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --folder /data_room --deal "Project Broadstone"
  python main.py --drive "https://drive.google.com/drive/folders/1abc" --deal "Project XXX"
  python main.py --folder /data_room --deal "Project XXX" --schema --excel
  python main.py --folder /data_room --deal "Project XXX" \\
      --signals-override "greenfield=true,hosting=true,existing_debt=false"
        """
    )

    # Mutually exclusive source
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--folder",
                     help="Local folder path containing data room documents")
    src.add_argument("--drive",
                     help="Google Drive folder URL or folder ID")

    # Deal metadata
    parser.add_argument("--deal",  default="Project XXX",
                        help="Deal / project name  (default: 'Project XXX')")
    parser.add_argument("--site",  default="",
                        help="Site address shown in document header")
    parser.add_argument("--mw",    default="",
                        help="Grid capacity in MW shown in document header")

    # Signal overrides
    valid_keys = ", ".join(SIGNALS.keys())
    parser.add_argument(
        "--signals-override", default="", metavar="KEY=BOOL,...",
        help=(f"Override detected signals. Format: 'key=true,key=false'. "
              f"Valid keys: {valid_keys}")
    )

    # Output options
    parser.add_argument("--schema", action="store_true",
                        help="Extract structured JSON deal schema from answers")
    parser.add_argument("--excel",  action="store_true",
                        help="Generate Excel underwriting model seed (implies --schema)")
    parser.add_argument("--quiet",  action="store_true",
                        help="Suppress per-question progress lines")

    args = parser.parse_args()

    site_info = {}
    if args.site: site_info["Site address"]  = args.site
    if args.mw:   site_info["Grid capacity"] = args.mw
    site_info = site_info or None

    overrides = parse_signals_override(args.signals_override)

    run_pipeline(
        folder_path      = args.folder,
        drive_url        = args.drive,
        deal_name        = args.deal,
        verbose          = not args.quiet,
        site_info        = site_info,
        signals_override = overrides,
        run_schema       = args.schema or args.excel,
        run_excel        = args.excel,
    )


if __name__ == "__main__":
    main()
