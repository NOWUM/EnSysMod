#!/bin/bash

cd "$(git rev-parse --show-toplevel)" || (
  echo "Couldn't find project folder. Please check your working dir."
  exit 1
)

conda --version || (echo "Conda not found. Exiting..." && exit 1)

conda env create -f requirements.yml -n EnSysMod-env || echo "Conda environment already exists. Activating..."
conda activate EnSysMod-env

# Update dependencies
conda env update --file requirements.yml --prune
