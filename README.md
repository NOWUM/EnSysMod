# Python Starter Repo
[![CI/CD main](https://github.com/V3lop5/python-starter/actions/workflows/main.yml/badge.svg)](https://github.com/V3lop5/python-starter/actions/workflows/main.yml)
[![Codecov](https://codecov.io/gh/v3lop5/python-starter/branch/main/graph/badge.svg)](https://codecov.io/gh/v3lop5/python-starter/branch/main)
[![GitHub license](https://img.shields.io/github/license/v3lop5/python-starter.svg)](https://github.com/v3lop5/python-starter/blob/main/LICENSE)
[![GitHub release](https://img.shields.io/github/release/v3lop5/python-starter.svg)](https://github.com/v3lop5/python-starter/releases/)


This repo helps you to kickstart your Python project. 

## Features

### Repository
- README.md with recommended structure
- Issue templates
- Pull Request template
- Release-Changelog template

### Python project
- Python 3.7, 3.8 or 3.9!
- Recommended project structure
- Tests with `pytest` 
- Linting with `flake8` 

### CI/CD
- Automated tests and linting
- Publish test results, linting and code coverage
- Annotations in pull requests
- Automated deployments
  - Latest release -> Production
  - Latest main branch -> Development
  - Any pull request -> Preview
- Release-changelog based on pull requests  
- Regenerate docs on release
- Publish docs to Readthedocs  

## Use this template
1. Click on button [Use this template](https://github.com/V3lop5/python-starter/generate)
2. Check the generated issue in the project and follow these steps.

### Workflow with git
Rule #1: No Commits to main!

Every feature or fix should be developed on branches for example `feature/new-rest-api` or `fix/status-500-on-empty-request`.

If a branch is ready for review a pull request can be opened. Tests and Linting are automated and report their results after a few seconds within the pull request. If tests and Linting passed a build is deployed to a preview env. This can easily be reviewed.

After approval the pull request is merged into main branch. From this branch a build is deployed to the dev env. All team members can use this working version of the project for their developments.

When all features are ready and merged into main a new release can be created within github. A changelog containing all pull requests is generated. In background by GitHub actions all assets for this release are generated and the docs are updated.
