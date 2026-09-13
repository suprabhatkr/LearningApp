#!/usr/bin/env bash
# ==============================================================================
# Ascend Learning Portal - Project Launcher Script
#
# Best Practices:
# 1. Isolates execution inside the project-local virtual environment (.venv).
# 2. Automatically bootstraps .venv and installs requirements if missing or updated.
# 3. Anchors working directory to this project folder to prevent any file spillover.
# 4. Uses 'exec' so OS signals (SIGINT/SIGTERM) pass directly to python/uvicorn.
# 5. Completely self-contained - zero mutation of outer shell or system python.
# ==============================================================================
set -euo pipefail

# 1. Resolve project root and anchor working directory inside this folder
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

VENV_DIR="$SCRIPT_DIR/.venv"
VENV_PYTHON="$VENV_DIR/bin/python"
VENV_PIP="$VENV_DIR/bin/pip"
REQ_FILE="$SCRIPT_DIR/requirements.txt"
HASH_FILE="$VENV_DIR/.requirements.sha256"

# Helper to compute SHA-256
compute_hash() {
    if command -v sha256sum >/dev/null 2>&1; then
        sha256sum "$1" | awk '{print $1}'
    else
        python3 -c "import hashlib, sys; print(hashlib.sha256(open(sys.argv[1], 'rb').read()).hexdigest())" "$1"
    fi
}

# 2. Verify host python3 availability
if ! command -v python3 >/dev/null 2>&1; then
    echo "[ERROR] python3 is required but not found in PATH." >&2
    exit 1
fi

# 3. Create .venv if it does not exist
if [ ! -d "$VENV_DIR" ] || [ ! -x "$VENV_PYTHON" ]; then
    echo "==> Local virtual environment (.venv) not found. Initializing at: $VENV_DIR"
    if ! python3 -m venv "$VENV_DIR"; then
        echo "[ERROR] Failed to create virtual environment with 'python3 -m venv'." >&2
        echo "Please ensure the python3-venv package is installed." >&2
        exit 1
    fi
    echo "==> Upgrading pip in local .venv..."
    PIP_DISABLE_PIP_VERSION_CHECK=1 "$VENV_PIP" install --upgrade pip --quiet || true
    echo "==> Virtual environment created successfully."
fi

# 4. Synchronize dependencies if requirements.txt exists and has changed
if [ -f "$REQ_FILE" ]; then
    CURRENT_HASH="$(compute_hash "$REQ_FILE")"
    SAVED_HASH=""
    if [ -f "$HASH_FILE" ]; then
        SAVED_HASH="$(cat "$HASH_FILE" 2>/dev/null || true)"
    fi

    if [ "$CURRENT_HASH" != "$SAVED_HASH" ]; then
        echo "==> Synchronizing dependencies from requirements.txt into local .venv..."
        PIP_DISABLE_PIP_VERSION_CHECK=1 "$VENV_PIP" install -r "$REQ_FILE" --quiet
        echo "$CURRENT_HASH" > "$HASH_FILE"
        echo "==> Dependencies synchronized successfully."
    fi
fi

# 5. Handle --setup-only flag directly
for arg in "$@"; do
    if [ "$arg" = "--setup-only" ]; then
        echo "==> Project virtual environment is fully set up and ready."
        exit 0
    fi
done

# 6. Execute run.py using the project's local virtual environment python
# Replaces current shell process so signals (SIGINT/Ctrl+C) pass directly to Python
exec "$VENV_PYTHON" "$SCRIPT_DIR/run.py" "$@"
