#!/bin/bash
# Start FastAPI backend and Vite dev server concurrently
set -e

# Start FastAPI in background
echo "Starting FastAPI backend..."
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000 &
API_PID=$!

# Start Vite dev server
echo "Starting Vite dev server..."
cd dashboard && npm run dev &
VITE_PID=$!

# Trap cleanup
trap "kill $API_PID $VITE_PID 2>/dev/null" EXIT

echo "Backend: http://localhost:8000"
echo "Dashboard: http://localhost:5173"
echo "Press Ctrl+C to stop both servers"

wait
