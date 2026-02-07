#!/bin/bash
# runer.sh
# This script runs three Python processes in parallel (background).

# Define the absolute path to the venv python binary
VENV_PYTHON="/home/path/bin/python3"

# Define the relative or absolute path to the Python script
PYTHON_WORKLIST="worklist.py"
PYTHON_DICOM="dicomitzador.py"
PYTHON_STORAGE="storage.py"

# --- EXECUTION ---

echo "Starting Worklist..."
$VENV_PYTHON $PYTHON_WORKLIST &

echo "Starting Dicomizer..."
$VENV_PYTHON $PYTHON_DICOM &

echo "Starting Storage..."
$VENV_PYTHON $PYTHON_STORAGE &

echo "All processes have been started. Waiting for them to finish (Ctrl+C to stop)."
wait
