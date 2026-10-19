#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
fi

source venv/bin/activate


export VYDEA_MOCK_MODEL="${VYDEA_MOCK_MODEL:-1}"
export VYDEA_LOW_VRAM="${VYDEA_LOW_VRAM:-1}"

echo "Starting Vydea backend on http://localhost:8000 (VYDEA_MOCK_MODEL=$VYDEA_MOCK_MODEL)"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
