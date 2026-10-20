
#!/usr/bin/env bash

set -Eeuo pipefail

echo "==================================================="
echo "  KINETIX - Autonomous Local Text-to-Video Studio"
echo "  Developed by JOJIN JOHN"
echo "==================================================="
echo

# Resolve the project root relative to this script.
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

BACKEND_DIR="$PROJECT_ROOT/backend"
FRONTEND_DIR="$PROJECT_ROOT/frontend"

BACKEND_PID=""
FRONTEND_PID=""

cleanup() {
    echo
    echo "Stopping Kinetix..."

    [[ -z "$BACKEND_PID" ]] || kill "$BACKEND_PID" 2>/dev/null || true
    [[ -z "$FRONTEND_PID" ]] || kill "$FRONTEND_PID" 2>/dev/null || true

    wait 2>/dev/null || true
}

trap cleanup EXIT INT TERM

# Validate project directories.
if [[ ! -d "$BACKEND_DIR" ]]; then
    echo "ERROR: Backend directory not found: $BACKEND_DIR"
    exit 1
fi

if [[ ! -d "$FRONTEND_DIR" ]]; then
    echo "ERROR: Frontend directory not found: $FRONTEND_DIR"
    exit 1
fi

# Find the Python virtual environment.
if [[ -f "$BACKEND_DIR/venv/bin/activate" ]]; then
    VENV="$BACKEND_DIR/venv"
elif [[ -f "$BACKEND_DIR/.venv/bin/activate" ]]; then
    VENV="$BACKEND_DIR/.venv"
else
    echo "ERROR: Python virtual environment not found."
    echo "Expected: backend/venv or backend/.venv"
    exit 1
fi

# Validate frontend dependencies.
if [[ ! -d "$FRONTEND_DIR/node_modules" ]]; then
    echo "ERROR: Frontend dependencies are missing."
    echo "Run 'npm install' inside the frontend directory first."
    exit 1
fi

echo "[1/3] Starting Kinetix Backend on http://127.0.0.1:8000 ..."

(
    cd "$BACKEND_DIR"
    source "$VENV/bin/activate"
    exec python -m uvicorn app.main:app \
        --host 127.0.0.1 \
        --port 8000 \
        --reload
) &

BACKEND_PID=$!

echo "[2/3] Starting Kinetix Frontend on http://localhost:3000 ..."

(
    cd "$FRONTEND_DIR"
    exec npm run dev -- --host 127.0.0.1
) &

FRONTEND_PID=$!

echo "[3/3] Waiting for the frontend to start..."

# Wait up to 30 seconds for the frontend to become available.
for ((i = 0; i < 30; i++)); do
    if ! kill -0 "$FRONTEND_PID" 2>/dev/null; then
        echo "ERROR: Frontend process exited unexpectedly."
        exit 1
    fi

    if curl -fsS http://127.0.0.1:3000/ >/dev/null 2>&1; then
        break
    fi

    sleep 1
done

if ! curl -fsS http://127.0.0.1:3000/ >/dev/null 2>&1; then
    echo "WARNING: Frontend did not respond within 30 seconds."
    echo "Check the frontend logs for errors."
else
    echo "Opening Kinetix Studio in your default browser..."
    xdg-open http://localhost:3000 >/dev/null 2>&1 &
fi

echo
echo "==================================================="
echo "  Kinetix is running!"
echo "  Studio UI: http://localhost:3000"
echo "  API Docs:  http://127.0.0.1:8000/docs"
echo "  Press Ctrl+C to stop."
echo "==================================================="

# Keep the launcher alive while both services run.
while kill -0 "$BACKEND_PID" 2>/dev/null &&
      kill -0 "$FRONTEND_PID" 2>/dev/null; do
    sleep 1
done

echo "ERROR: One of the services has stopped."
exit 1

