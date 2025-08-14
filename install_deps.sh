#!/bin/bash

VENV_DIR="./venv"
REQUIREMENTS_FILE="./requirements.txt"
LAST_INSTALL_HASH_FILE="./.last_requirements_hash"

# Check if virtual environment exists, if not, create it
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment in $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
    VENV_CREATED=true
else
    VENV_CREATED=false
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Calculate current hash of requirements.txt
CURRENT_HASH=$(sha256sum "$REQUIREMENTS_FILE" | awk '{print $1}')

# Read last installed hash
LAST_HASH=""
if [ -f "$LAST_INSTALL_HASH_FILE" ]; then
    LAST_HASH=$(cat "$LAST_INSTALL_HASH_FILE")
fi

# Check if requirements.txt has changed or venv was just created
if [ "$CURRENT_HASH" != "$LAST_HASH" ] || [ "$VENV_CREATED" = true ]; then
    echo "New or updated packages detected in $REQUIREMENTS_FILE, or virtual environment newly created. Installing/updating dependencies..."
    pip install -r "$REQUIREMENTS_FILE"
    # Save current hash for future checks
    echo "$CURRENT_HASH" > "$LAST_INSTALL_HASH_FILE"
else
    echo "No new packages detected in $REQUIREMENTS_FILE. Dependencies are up to date."
fi

# Deactivate the venv after installation if it was activated by this script
deactivate 2>/dev/null || true

echo ""
echo "Virtual environment setup complete."
echo "To activate the virtual environment, run: source $VENV_DIR/bin/activate"
