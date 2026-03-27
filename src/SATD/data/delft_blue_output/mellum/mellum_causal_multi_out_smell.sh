#!/bin/sh
#
#SBATCH --job-name="mellum_causal_multi_out_smell"
#SBATCH --partition=gpu
#SBATCH --time=07:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --gpus-per-task=1
#SBATCH --mem-per-cpu=4G
#SBATCH --account=education-eemcs-courses-cse3000

# Load modules:
module load 2023r1
module load miniconda3

# Activate environment:
conda activate /scratch/lcwitte/env-satd/

export PYTHONPATH="/home/lcwitte/ML4SE-toolkit/src:$PYTHONPATH"
MODEL_NAME="MellumBase4B"  # "SmolLM135M" or "StarCoder2_3B" or "MellumBase4B"
# Run your Python script with the model name:
srun python /home/lcwitte/ML4SE-toolkit/src/results/code_gen/causal_multi_out_smell.py "$MODEL_NAME"

# Deactivate environment:
conda deactivate

