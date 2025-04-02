#!/usr/bin/bash
# Bash script to run micasa-animation.py and save output
#

module purge
module load python/GEOSpyD/Min24.4.0-0_py3.12

# Make directory for test
mkdir -p $1

python -u micasa-animation.py $1 | tee $1/"output.log"
