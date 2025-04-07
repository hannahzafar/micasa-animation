#!/usr/bin/bash
# Bash script to run micasa-animation.py and save output
#

# Ensure arguments are passed
if [[ $# -ne 2 ]]; then
    echo "Usage: $0 <log_directory> <description>"
    exit 1
fi

# Fail if the directory already exists
if [[ -d "$1" ]]; then
    echo "Error: Directory '$1' already exists. Choose a different directory."
    exit 1
fi

module purge
module load python/GEOSpyD/Min24.4.0-0_py3.12

# Make directory for test
OUTPUT_DIR="frames/${1}"
mkdir -p "$OUTPUT_DIR"
LOG_FILE="$OUTPUT_DIR/output.log"

python -u micasa-animation.py "$OUTPUT_DIR" | tee "$LOG_FILE"
echo -e "\n Run Description: $2" >> "$LOG_FILE" 
