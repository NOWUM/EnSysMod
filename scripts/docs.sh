#!/bin/bash

cd "$(git rev-parse --show-toplevel)" || (
  echo "Couldn't find project folder. Please check your working dir."
  exit 1
)

cd docs || (
  echo "Couldn't find docs folder. Please check your working dir."
  exit 1
)

make html

echo "HTML documentation is here: file://$(pwd)/_build/html/index.html"
