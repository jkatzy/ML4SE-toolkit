#!/bin/sh
#
#SBATCH --job-name="code_gen-in_star"
#SBATCH --partition=gpu
#SBATCH --time=00:50:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --gpus-per-task=1
#SBATCH --mem-per-cpu=2G
#SBATCH --account=education-eemcs-courses-cse3000

# Load modules:
module load 2023r1
module load miniconda3

# Activate environment:
conda activate /scratch/lcwitte/env-satd/

# Run your python file:
srun python ../src/code_gen_causal-in_star.py

# Deactivate environment:
conda deactivate

