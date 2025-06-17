#!/bin/bash
set -e

VENV_DIR=".venv-s3"

# Create the virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Creating virtual environment..."
    if ! python3 -m venv "$VENV_DIR"; then
        echo "❌ Failed to create virtual environment. Install it with:"
        echo "    sudo apt install python3-venv -y"
        exit 1
    fi
fi

# Check if the activation file exists
if [ ! -f "$VENV_DIR/bin/activate" ]; then
    echo "❌ Virtual environment activation file is missing."
    exit 1
fi

# Activate the venv and install dependencies
source "$VENV_DIR/bin/activate"
pip install --upgrade pip
pip install boto3 python-dotenv

# Run the Python script
python minio_storage_finops.py
