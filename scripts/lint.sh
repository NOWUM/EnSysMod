#!/bin/bash

cd "$(git rev-parse --show-toplevel)" || (
  echo "Couldn't find project folder. Please check your working dir."
  exit 1
)

ruff check

echo "Lint complete. Check for code smells above."
