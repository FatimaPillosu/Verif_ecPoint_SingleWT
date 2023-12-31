#!/bin/bash

#SBATCH --job-name=BSrel_BS
#SBATCH --output=LogATOS/BSrel_BS-%J.out
#SBATCH --error=LogATOS/BSrel_BS-%J.out
#SBATCH --cpus-per-task=64
#SBATCH --mem=128G
#SBATCH --qos=nf
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=fatima.pillosu@ecmwf.int

# INPUTS
VRT_list=${1}
SystemFC_list=${2}

# CODE
python3 02_Compute_BSrel_BS.py ${VRT_list} ${SystemFC_list}