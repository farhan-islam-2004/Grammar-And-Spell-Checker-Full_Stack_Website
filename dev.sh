#!/usr/bin/env bash
# dev.sh — stop any running app.py on the chosen PORT and restart the Flask app from the venv
# Usage: ./dev.sh [PORT]

set -euo pipefail
PORT=${1:-5001}
VENV_PY=.venv/bin/python
APP=app.py

echo "Stopping any process listening on port ${PORT}..."
PIDS=$(lsof -ti tcp:${PORT} || true)
if [[ -n "$PIDS" ]]; then
  echo "Found PIDs: $PIDS"
  echo "Killing..."
  kill $PIDS || true
  sleep 0.3
  # Ensure they are gone
  PIDS=$(lsof -ti tcp:${PORT} || true)
  if [[ -n "$PIDS" ]]; then
    echo "Force-killing PIDs: $PIDS"
    kill -9 $PIDS || true
    sleep 0.2
  fi
else
  echo "No process found on port ${PORT}"
fi

echo "Starting app on port ${PORT} using ${VENV_PY} ${APP}"
# Start in background
PORT=${PORT} ${VENV_PY} ${APP} &
PID=$!
sleep 0.6
# Quick sanity checks
if lsof -i :${PORT} -sTCP:LISTEN -Pn >/dev/null 2>&1; then
  echo "App started (PID=${PID}) and listening on port ${PORT}"
  echo "GET / ->"
  curl -sS -I http://127.0.0.1:${PORT}/ | sed -n '1,6p'
else
  echo "Failed to start app. Check logs."
  exit 1
fi

echo "Done. Use 'tail -n +1 /tmp/flask_dev_${PID}.log' to view logs" || true
