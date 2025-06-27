#!/bin/sh
#
#SBATCH --job-name="code_gen_causal-in_smol"
#SBATCH --partition=gpu
#SBATCH --time=01:00:00
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

MODEL_NAME="SmolLM135M"  # or "StarCoder2_3B" or "MellumBase4B"
# Run your Python script with the model name:
srun python ../src/code_gen_causal_in_smell.py "$MODEL_NAME"

# Deactivate environment:
conda deactivate

