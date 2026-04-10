"""
BTSF DDQ Automation — Flask Web Interface
Run with : python app.py
Access   : http://localhost:5000
"""

import os
import sys
import uuid
import threading
import shutil
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file, abort

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR    = Path(__file__).parent
DDQ_APP_DIR = BASE_DIR.parent / "ddq_app"
UPLOAD_DIR  = BASE_DIR / "uploads"
OUTPUT_DIR  = BASE_DIR / "output"

UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Add ddq_app to the Python path
sys.path.insert(0, str(DDQ_APP_DIR))

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024  # 100 MB max upload

# ── In-memory job store ───────────────────────────────────────────────────────
jobs = {}   # job_id -> { status, progress, message, output_path, error }


# ── Accepted file extensions ──────────────────────────────────────────────────
ALLOWED = {".pdf", ".docx", ".doc", ".xlsx", ".xls", ".txt", ".csv", ".md"}

def allowed_file(filename: str) -> bool:
    return Path(filename).suffix.lower() in ALLOWED


# ── Worker (runs in a separate thread) ────────────────────────────────────────

def run_ddq_job(job_id: str, folder_path: str, deal_name: str,
                location: str, signals_override: str):
    """Run the DDQ pipeline in a background thread."""
    try:
        jobs[job_id]["status"]   = "running"
        jobs[job_id]["message"]  = "Extracting documents..."
        jobs[job_id]["progress"] = 10

        # Key from Render env var (fallback to form input if provided)
        api_key = os.getenv("ANTHROPIC_API_KEY") or jobs[job_id].get("api_key", "")
        if not api_key:
            raise ValueError("Anthropic API key not configured. Set ANTHROPIC_API_KEY in the Render environment variables.")
        os.environ["ANTHROPIC_API_KEY"] = api_key

        from core.ingestion import ingest_folder
        from core.signals   import detect_signals
        from core.questions import assemble_questions
        from core.generator import generate_answers
        from core.writer    import export_docx
        from main           import parse_signals_override

        # Step 1
        chunks = ingest_folder(folder_path)
        jobs[job_id]["message"]  = f"{len(chunks)} chunks extracted — detecting signals..."
        jobs[job_id]["progress"] = 25

        # Step 2
        signals = detect_signals(chunks)
        if signals_override:
            overrides = parse_signals_override(signals_override)
            signals.update(overrides)

        active = [k for k, v in signals.items() if v]
        jobs[job_id]["message"]  = f"Signals: {', '.join(active) or 'none'} — assembling questions..."
        jobs[job_id]["progress"] = 40
        jobs[job_id]["signals"]  = signals

        # Step 3
        questions = assemble_questions(signals)
        jobs[job_id]["message"]  = f"{len(questions)} questions — generating answers..."
        jobs[job_id]["progress"] = 50

        # Step 4 — per-question progress callback
        answers = []
        total   = len(questions)
        for i, q in enumerate(questions, 1):
            ans_list = generate_answers([q], chunks, verbose=False)
            answers.extend(ans_list)
            pct = 50 + int((i / total) * 40)
            jobs[job_id]["progress"] = pct
            jobs[job_id]["message"]  = f"Question {i}/{total} — {q.qid}..."

        # Step 5
        jobs[job_id]["message"]  = "Generating Word document..."
        jobs[job_id]["progress"] = 92

        site_info = {}
        if location:
            site_info["Location"] = location

        # Force output into our folder
        import config as cfg
        cfg.OUTPUT_DIR = str(OUTPUT_DIR)

        output_path = export_docx(answers, signals, deal_name, site_info or None)

        jobs[job_id]["status"]      = "done"
        jobs[job_id]["progress"]    = 100
        jobs[job_id]["message"]     = "DDQ generated successfully."
        jobs[job_id]["output_path"] = output_path
        jobs[job_id]["output_name"] = Path(output_path).name

        # Statistics
        from collections import Counter
        counts = Counter(a.confidence for a in answers)
        jobs[job_id]["stats"] = {
            "total":    len(answers),
            "answered": counts.get("answered", 0),
            "partial":  counts.get("partial",  0),
            "gap":      counts.get("gap",      0),
        }

    except Exception as e:
        jobs[job_id]["status"]  = "error"
        jobs[job_id]["message"] = str(e)
        jobs[job_id]["error"]   = str(e)
    finally:
        # Clean up the temporary upload folder
        shutil.rmtree(folder_path, ignore_errors=True)


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    """Receive the form, save files, start the job."""
    deal_name        = request.form.get("deal_name", "Project XXX").strip()
    location         = request.form.get("site", "").strip()
    signals_override = request.form.get("signals_override", "").strip()
    files            = request.files.getlist("documents")

    if not files or all(f.filename == "" for f in files):
        return jsonify({"error": "No documents uploaded."}), 400

    # Save files into a temporary folder
    job_id     = str(uuid.uuid4())[:8]
    job_folder = UPLOAD_DIR / job_id
    job_folder.mkdir()

    saved = 0
    for f in files:
        if f and f.filename and allowed_file(f.filename):
            dest = job_folder / Path(f.filename).name
            f.save(str(dest))
            saved += 1

    if saved == 0:
        shutil.rmtree(str(job_folder), ignore_errors=True)
        return jsonify({"error": "No valid files (PDF, DOCX, XLSX accepted)."}), 400

    # Initialise job
    jobs[job_id] = {
        "status":   "queued",
        "progress": 0,
        "message":  f"{saved} file(s) received — starting...",
    }

    # Launch in a separate thread
    t = threading.Thread(
        target=run_ddq_job,
        args=(job_id, str(job_folder), deal_name, location, signals_override),
        daemon=True
    )
    t.start()

    return jsonify({"job_id": job_id})


@app.route("/status/<job_id>")
def status(job_id):
    """Return the job status (polling endpoint)."""
    job = jobs.get(job_id)
    if not job:
        return jsonify({"error": "Job not found."}), 404
    return jsonify({
        "status":      job.get("status"),
        "progress":    job.get("progress", 0),
        "message":     job.get("message", ""),
        "output_name": job.get("output_name"),
        "stats":       job.get("stats"),
        "signals":     job.get("signals"),
        "error":       job.get("error"),
    })


@app.route("/download/<job_id>")
def download(job_id):
    """Download the generated Word file."""
    job = jobs.get(job_id)
    if not job or job.get("status") != "done":
        abort(404)
    path = job.get("output_path")
    if not path or not Path(path).exists():
        abort(404)
    return send_file(path, as_attachment=True,
                     download_name=job.get("output_name"))


# ── Entrypoint ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "="*55)
    print("  BTSF DDQ Automation — Web Interface (Flask)")
    print("  Open your browser at: http://localhost:5000")
    print("="*55 + "\n")
    app.run(debug=False, host="0.0.0.0", port=5000)
