#!/usr/bin/env bash
# ==============================================================================
# Ascend LearningApp - Virtual Environment Activation Helper
#
# Best Practice Usage:
# 1. Interactive Subshell (Recommended - zero impact on outer shell):
#      ./activate.sh
#    Spawns an isolated subshell with the project's .venv active and CWD inside project.
#    Type 'exit' to return to your outer shell untouched.
#
# 2. Source into current shell:
#      source activate.sh
#    Activates .venv in current session. Run 'deactivate' when done.
# ==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"
VENV_PYTHON="$VENV_DIR/bin/python"
VENV_PIP="$VENV_DIR/bin/pip"
REQ_FILE="$SCRIPT_DIR/requirements.txt"
HASH_FILE="$VENV_DIR/.requirements.sha256"

compute_hash() {
    if command -v sha256sum >/dev/null 2>&1; then
        sha256sum "$1" | awk '{print $1}'
    else
        python3 -c "import hashlib, sys; print(hashlib.sha256(open(sys.argv[1], 'rb').read()).hexdigest())" "$1"
    fi
}

# Ensure host python3 is available
if ! command -v python3 >/dev/null 2>&1; then
    echo "[ERROR] python3 is required but not found in PATH." >&2
    return 1 2>/dev/null || exit 1
fi

# Ensure .venv exists
if [ ! -d "$VENV_DIR" ] || [ ! -x "$VENV_PYTHON" ]; then
    echo "==> Local virtual environment (.venv) not found. Setting up at: $VENV_DIR"
    if ! python3 -m venv "$VENV_DIR"; then
        echo "[ERROR] Failed to create virtual environment with 'python3 -m venv'." >&2
        return 1 2>/dev/null || exit 1
    fi
    PIP_DISABLE_PIP_VERSION_CHECK=1 "$VENV_PIP" install --upgrade pip --quiet || true
    echo "==> Virtual environment created successfully."
fi

# Ensure requirements are synced
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

# Detect whether this script is being sourced or executed
(return 0 2>/dev/null) && SOURCED=1 || SOURCED=0

if [ "$SOURCED" -eq 1 ]; then
    # Sourced: activate in current shell session
    # shellcheck disable=SC1091
    source "$VENV_DIR/bin/activate"
    echo "==> Activated LearningApp virtualenv (.venv) in current shell."
    echo "==> Run 'deactivate' to restore your previous environment."
else
    # Executed: spawn isolated subshell with .venv active
    echo "==> Entering isolated shell for LearningApp (.venv)."
    echo "==> Working directory: $SCRIPT_DIR"
    echo "==> Any commands run here use this project's isolated environment."
    echo "==> Type 'exit' to leave without modifying your outer environment."
    echo ""

    # Launch interactive bash subshell with .venv activated and custom prompt indicator
    exec bash --init-file <(cat <<EOF
if [ -f ~/.bashrc ]; then
    source ~/.bashrc
fi
cd "$SCRIPT_DIR"
source "$VENV_DIR/bin/activate"
PS1="\[\e[1;36m\](LearningApp-venv)\[\e[0m\] \w \\$ "
EOF
    )
fi
