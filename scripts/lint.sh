#!/bin/bash

cd "$(git rev-parse --show-toplevel)" || (
  echo "Couldn't find project folder. Please check your working dir."
  exit 1
)

flake8 ./ensysmod
flake8 ./tests

echo "Flake8 complete. Check for code smells above."
