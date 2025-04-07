#!/usr/bin/env bash
# Wrapper script to run sbatch on micasa-animation-batch.sh

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

# Create log directory
mkdir -p "frames/${1}"

# Run sbatch script with args
sbatch <<EOT
#!/usr/bin/bash
# Bash script to run micasa-animation.py and save output
#SBATCH --account=s1460
#SBATCH --time=0:10:00
#SBATCH --output=${1}/slurm-output-%j.log  
# Script to run micasa-animation.py in a SLURM job

module purge
module load python/GEOSpyD/Min24.4.0-0_py3.12

LOG_FILE="$1/output.log"

python -u micasa-animation.py "$1" | tee "$LOG_FILE"
echo -e "\n Run Description: $2" >> "$LOG_FILE" 
EOT
