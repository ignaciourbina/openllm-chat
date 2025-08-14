#!/bin/bash

# Navigate to the project root
PROJECT_ROOT=$(dirname "$0")
cd "$PROJECT_ROOT" || exit

# --- Configuration ---
VENV_BIN="./venv/bin"
FLASK_PORT=${1:-8888}
OPENLLM_PORT=3000
OPENLLM_PID=""

# --- Cleanup Function ---
cleanup() {
    echo -e "\nShutting down..."
    if [ -n "$OPENLLM_PID" ]; then
        echo "Stopping background OpenLLM server (PID: $OPENLLM_PID)"
        kill "$OPENLLM_PID"
    fi
    FLASK_PID=$(lsof -t -i:"$FLASK_PORT" 2>/dev/null)
    if [ -n "$FLASK_PID" ]; then
        echo "Stopping Flask server (PID: $FLASK_PID)"
        kill "$FLASK_PID"
    fi
    echo "Cleanup complete."
    exit
}

trap cleanup SIGINT SIGTERM EXIT

# --- Main Script ---

# Activate virtual environment (still good practice)
source "$VENV_BIN/activate"

# Check if OpenLLM server is running
echo "Checking for OpenLLM server on port $OPENLLM_PORT..."
if ! lsof -i:"$OPENLLM_PORT" > /dev/null; then
    echo "OpenLLM server not found. Starting it in the background..."
    # Ensure dependencies are installed
    ./install_deps.sh > /dev/null
    
    # Start the server using the venv executable and get its PID
    "$VENV_BIN/openllm" serve models/TinyLlama-1.1B-Chat-v1.0 &
    OPENLLM_PID=$!
    echo "OpenLLM server starting with PID: $OPENLLM_PID"
    
    # Wait for the server to be ready
    echo "Waiting for OpenLLM server to initialize (this may take a moment)..."
    while ! lsof -i:"$OPENLLM_PORT" > /dev/null; do
        if ! ps -p $OPENLLM_PID > /dev/null; then
            echo "OpenLLM server failed to start."
            exit 1
        fi
        sleep 1
    done
    echo "OpenLLM server is ready."
else
    echo "OpenLLM server is already running."
fi

# Start the Flask web server using the venv python
echo "Starting Flask web server on port $FLASK_PORT..."
export PORT=$FLASK_PORT
export OPENLLM_MODEL="TinyLlama/TinyLlama-1.1B-Chat-v1.0"
cd app
"$VENV_BIN/python" app.py

# The script will wait here until you press Ctrl+C
# The 'trap' command will then automatically call the 'cleanup' function