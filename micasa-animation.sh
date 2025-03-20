#!/usr/bin/env bash
#SBATCH --account=s1460
#SBATCH --time=0:01:00
#SBATCH --constraint="[cas|sky|mil]”

module purge
module load python/GEOSpyD/Min24.4.0-0_py3.12

mamba run -n data-analysis python $NOBACKUP/ghgc/micasa/micasa-animation/micasa-animation.py
