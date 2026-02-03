#!/bin/bash
# Script to run the daily skills report

echo "Running daily skills report generation..."

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to the scripts directory
cd "$SCRIPT_DIR"

# Run the Python script to generate the daily report
python3 check_new_skills.py

echo "Daily skills report generation completed."