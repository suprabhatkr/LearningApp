#!/usr/bin/env python3
"""Run script for Ascend - Senior SDE Learn Hub.

Automatically ensures execution inside the project's local virtual environment (.venv)
and starts the uvicorn server on default port 8090.
"""
import argparse
import hashlib
import os
import subprocess
import sys
from pathlib import Path

# --- Directory & Environment Anchoring ---
PROJECT_ROOT = Path(__file__).resolve().parent
VENV_DIR = PROJECT_ROOT / ".venv"
VENV_PYTHON = VENV_DIR / "bin" / "python"
VENV_PIP = VENV_DIR / "bin" / "pip"
REQ_FILE = PROJECT_ROOT / "requirements.txt"
HASH_FILE = VENV_DIR / ".requirements.sha256"

# Ensure current working directory is anchored to the project directory
os.chdir(PROJECT_ROOT)
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def compute_requirements_hash() -> str:
    """Compute SHA-256 hash of requirements.txt."""
    if not REQ_FILE.is_file():
        return ""
    h = hashlib.sha256()
    h.update(REQ_FILE.read_bytes())
    return h.hexdigest()


def ensure_local_venv():
    """Ensure the local .venv exists and dependencies are in sync."""
    # 1. Create .venv if missing
    if not VENV_PYTHON.is_file():
        print(f"==> Local virtual environment (.venv) not found. Initializing at: {VENV_DIR}...", flush=True)
        try:
            subprocess.check_call([sys.executable, "-m", "venv", str(VENV_DIR)])
        except Exception as e:
            print(f"[ERROR] Failed to create virtual environment: {e}\nPlease ensure python3-venv is installed.", file=sys.stderr)
            sys.exit(1)

        try:
            env = {**os.environ, "PIP_DISABLE_PIP_VERSION_CHECK": "1"}
            subprocess.check_call([str(VENV_PIP), "install", "--upgrade", "pip", "--quiet"], env=env)
        except Exception:
            pass

    # 2. Sync requirements if needed
    if REQ_FILE.is_file():
        req_hash = compute_requirements_hash()
        saved_hash = HASH_FILE.read_text().strip() if HASH_FILE.is_file() else ""
        if req_hash != saved_hash:
            print("==> Synchronizing dependencies from requirements.txt into local .venv...", flush=True)
            env = {**os.environ, "PIP_DISABLE_PIP_VERSION_CHECK": "1"}
            try:
                subprocess.check_call([str(VENV_PIP), "install", "-r", str(REQ_FILE), "--quiet"], env=env)
                HASH_FILE.write_text(req_hash)
                print("==> Dependencies synchronized successfully.", flush=True)
            except subprocess.CalledProcessError as e:
                print(f"[ERROR] Dependency installation failed with exit code {e.returncode}.", file=sys.stderr)
                sys.exit(e.returncode)


# --- Virtual Environment Self-Bootstrap Guard ---
# Ensures this project ALWAYS runs inside its own isolated .venv,
# whether invoked as 'python3 run.py', './run.py', or from an outer virtualenv.
if Path(sys.prefix).resolve() != VENV_DIR.resolve():
    ensure_local_venv()

    # If --setup-only was passed, exit after setting up
    if "--setup-only" in sys.argv:
        print("==> Project virtual environment is fully set up and ready.")
        sys.exit(0)

    # Re-execute under the project's local virtual environment python
    new_env = os.environ.copy()
    new_env["VIRTUAL_ENV"] = str(VENV_DIR)
    new_env["PATH"] = f"{VENV_DIR / 'bin'}:{new_env.get('PATH', '')}"
    new_env["PYTHONPATH"] = str(PROJECT_ROOT)
    os.execve(str(VENV_PYTHON), [str(VENV_PYTHON)] + sys.argv, new_env)

# --- Application Startup (Executed strictly inside .venv) ---
import uvicorn
from app.config import settings


def print_env_diagnostics():
    """Print diagnostics showing environment isolation."""
    print("==================================================")
    print("  Ascend Learning Portal - Environment Status     ")
    print("==================================================")
    print(f"  Project Root:        {PROJECT_ROOT}")
    print(f"  Active Python:       {sys.executable}")
    print(f"  Virtualenv Prefix:   {sys.prefix}")
    print(f"  Expected .venv:      {VENV_DIR}")
    is_isolated = Path(sys.prefix).resolve() == VENV_DIR.resolve()
    print(f"  Isolated inside .venv: {'YES (✓)' if is_isolated else 'NO (✗)'}")
    print(f"  Default Host / Port: {settings.HOST}:{settings.PORT}")
    print(f"  Database URL:        {settings.DATABASE_URL}")
    print("==================================================")


def main():
    parser = argparse.ArgumentParser(description=f"Start {settings.APP_NAME}")
    parser.add_argument(
        "--port",
        type=int,
        default=settings.PORT,
        help=f"Port to run the server on (default: {settings.PORT})",
    )
    parser.add_argument(
        "--host",
        type=str,
        default=settings.HOST,
        help=f"Host interface to bind to (default: {settings.HOST})",
    )
    parser.add_argument(
        "--reload",
        dest="reload",
        action="store_true",
        default=True,
        help="Enable auto-reload on code changes (default: enabled)",
    )
    parser.add_argument(
        "--no-reload",
        dest="reload",
        action="store_false",
        help="Disable auto-reload",
    )
    parser.add_argument(
        "--check-env",
        action="store_true",
        help="Verify and print local virtual environment status and exit",
    )
    parser.add_argument(
        "--setup-only",
        action="store_true",
        help="Setup local virtual environment and install requirements without starting the server",
    )

    args = parser.parse_args()

    if args.check_env:
        print_env_diagnostics()
        sys.exit(0)

    if args.setup_only:
        print("==> Project virtual environment is fully set up and ready.")
        sys.exit(0)

    print(f"Starting {settings.APP_NAME}...")
    print(f"Access learning portal at: http://{args.host}:{args.port}")
    uvicorn.run("app.main:app", host=args.host, port=args.port, reload=args.reload)


if __name__ == "__main__":
    main()
