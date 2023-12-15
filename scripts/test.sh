#!/bin/bash

cd "$(git rev-parse --show-toplevel)" || (
  echo "Couldn't find project folder. Please check your working dir."
  exit 1
)

pytest --cov=./ensysmod --cov-branch --cov-report=html ./tests

echo "Coverage report is here: file://$(pwd)/htmlcov/index.html"
