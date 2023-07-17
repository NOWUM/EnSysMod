#!/bin/bash

cd "$(git rev-parse --show-toplevel)" || (
  echo "Couldn't find project folder. Please check your working dir."
  exit 1
)

pip install --upgrade --upgrade-strategy eager -r requirements-dev.txt -e .
