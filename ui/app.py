from __future__ import annotations

from flask import Flask, abort, jsonify, render_template, request, send_file, send_from_directory
from flask_cors import CORS
import glob
import os
import subprocess
import threading
import time
from pathlib import Path

# ======================
# PATH CONFIG
# ======================
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

OUTPUT_DIR = PROJECT_ROOT / "output"
DATASETS_DIR = PROJECT_ROOT / "datasets"
LOG_DIR = OUTPUT_DIR / "ui_logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# ======================
# FLASK INIT
# ======================
app = Flask(__name__, template_folder="templates")
CORS(app)

# ======================
# STATE
# ======================
STATE_LOCK = threading.Lock()
STATE = {
    "robot": {"status": "idle", "pid": None, "returncode": None, "log": None},
    "odm": {"status": "idle", "pid": None, "returncode": None, "log": None},
    "pipeline": {"status": "idle", "message": "", "log": None},
}

env = os.environ.copy()
env["PYTHONUNBUFFERED"] = "1"


# ======================
# UTILS
# ======================
def now_tag():
    return time.strftime("%Y%m%d_%H%M%S")


def set_state(section, **kwargs):
    with STATE_LOCK:
        STATE[section].update(kwargs)


def snapshot():
    with STATE_LOCK:
        return {k: dict(v) for k, v in STATE.items()}


def safe_rel(path: Path):
    try:
        return path.relative_to(PROJECT_ROOT).as_posix()
    except Exception:
        return str(path)


def tail_file(path: Path, n=200):
    if not path.exists():
        return ""
    try:
        return "\n".join(path.read_text(errors="ignore").splitlines()[-n:])
    except Exception:
        return ""


# ======================
# MODEL FINDER
# ======================
def find_models():
    models = []
    if not OUTPUT_DIR.exists():
        return models

    patterns = [
        str(OUTPUT_DIR / "output_*" / "odm_texturing" / "*.obj"),
        str(OUTPUT_DIR / "output_*" / "odm_texturing" / "*.glb"),
        str(OUTPUT_DIR / "output_*" / "odm_texturing" / "*.gltf"),
    ]

    seen = set()

    for p in patterns:
        for m in sorted(glob.glob(p)):
            path = Path(m)
            rel = safe_rel(path)

            if rel in seen:
                continue
            seen.add(rel)

            models.append({
                "name": path.name,
                "path": rel,
                "task": path.parents[1].name
            })

    return models


# ======================
# FILE SERVER (IMPORTANT FIX)
# ======================
@app.route("/api/files/<path:filename>")
def serve_files(filename):
    return send_from_directory(PROJECT_ROOT, filename)


@app.route("/api/model")
def api_model():
    path = request.args.get("path", "")
    if not path:
        abort(400)

    requested = (PROJECT_ROOT / path).resolve()

    if PROJECT_ROOT not in requested.parents:
        abort(403)

    if not requested.exists():
        abort(404)

    return send_file(requested)


# ======================
# MODELS API
# ======================
@app.route("/api/models")
def api_models():
    return jsonify(find_models())


# ======================
# STATUS
# ======================
@app.route("/api/status")
def status():
    snap = snapshot()

    for s in ["robot", "odm", "pipeline"]:
        log = snap[s].get("log")
        snap[s]["tail"] = tail_file(PROJECT_ROOT / log) if log else ""

    return jsonify(snap)


# ======================
# PROCESS LAUNCHER
# ======================
def launch_process(section, label, cmd, cwd, log_path: Path):
    log_file = log_path.open("a", buffering=1, encoding="utf-8")

    log_file.write(f"\n===== {label} @ {now_tag()} =====\n")
    log_file.flush()

    process = subprocess.Popen(
        cmd,
        cwd=str(cwd),
        stdout=log_file,
        stderr=log_file,
        text=True,
        env=env
    )

    set_state(section,
              status="running",
              pid=process.pid,
              returncode=None,
              log=safe_rel(log_path))

    return process


# ======================
# PIPELINE
# ======================
def run_pipeline():
    pipe_log = LOG_DIR / f"pipeline_{now_tag()}.log"
    robot_log = LOG_DIR / f"robot_{now_tag()}.log"
    odm_log = LOG_DIR / f"odm_{now_tag()}.log"

    set_state("pipeline", status="running", message="Running robot", log=safe_rel(pipe_log))

    robot = launch_process(
        "robot",
        "Robot",
        ["python3", str(PROJECT_ROOT / "ur.py")],
        PROJECT_ROOT,
        robot_log
    )

    rc = robot.wait()
    set_state("robot", status="finished" if rc == 0 else "failed", returncode=rc)

    if rc != 0:
        set_state("pipeline", status="failed", message="Robot failed")
        return

    set_state("pipeline", status="running", message="Running ODM")

    odm = launch_process(
        "odm",
        "ODM",
        ["bash", str(PROJECT_ROOT / "run_odm.sh"), str(DATASETS_DIR)],
        PROJECT_ROOT,
        odm_log
    )

    rc2 = odm.wait()
    set_state("odm", status="finished" if rc2 == 0 else "failed", returncode=rc2)

    if rc2 == 0:
        set_state("pipeline", status="completed", message="Done")
    else:
        set_state("pipeline", status="failed", message="ODM failed")


# ======================
# ROUTES CONTROL
# ======================
@app.route("/api/start_robot", methods=["POST"])
def start_robot():
    log_path = LOG_DIR / f"robot_{now_tag()}.log"

    launch_process(
        "robot",
        "Robot",
        ["python3", str(PROJECT_ROOT / "ur.py")],
        PROJECT_ROOT,
        log_path
    )

    return jsonify({"status": "started"})


@app.route("/api/start_odm", methods=["POST"])
def start_odm():
    log_path = LOG_DIR / f"odm_{now_tag()}.log"

    launch_process(
        "odm",
        "ODM",
        ["bash", str(PROJECT_ROOT / "run_odm.sh"), str(DATASETS_DIR)],
        PROJECT_ROOT,
        log_path
    )

    return jsonify({"status": "started"})


@app.route("/api/run_all", methods=["POST"])
def run_all():
    with STATE_LOCK:
        if STATE["pipeline"]["status"] == "running":
            return jsonify({"status": "already_running"}), 409

    threading.Thread(target=run_pipeline, daemon=True).start()
    return jsonify({"status": "started"})


@app.route("/api/stop_all", methods=["POST"])
def stop_all():
    with STATE_LOCK:
        pids = [STATE["robot"]["pid"], STATE["odm"]["pid"]]

    for pid in pids:
        if pid:
            try:
                subprocess.run(["kill", str(pid)])
            except:
                pass

    set_state("robot", status="idle", pid=None)
    set_state("odm", status="idle", pid=None)
    set_state("pipeline", status="idle", message="stopped")

    return jsonify({"status": "stopped"})


# ======================
# MAIN
# ======================
@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)