#!/bin/bash
# stopper.sh
# Stops the three background Python processes started by runner.sh.

echo "Attempting to stop all DICOM processing scripts..."

# Use pkill -f to find and terminate processes by the command line (script name).
# The -f flag searches the full command line, which includes the script name.

# 1. Stop Worklist
pkill -f "worklist.py"
echo "Status: Sent termination signal to worklist.py"

# 2. Stop Dicomizer
pkill -f "dicomitzador.py"
echo "Status: Sent termination signal to dicomitzador.py"

# 3. Stop Storage
pkill -f "storage.py"
echo "Status: Sent termination signal to storage.py"

echo "Cleanup attempt complete. Use 'ps aux | grep python' to verify."
