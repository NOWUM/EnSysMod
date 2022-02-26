# EnSysMod
[![CI/CD main](https://github.com/NOWUM/EnSysMod/actions/workflows/main.yml/badge.svg)](https://github.com/NOWUM/EnSysMod/actions/workflows/main.yml)
[![Codecov](https://codecov.io/gh/NOWUM/EnSysMod/branch/main/graph/badge.svg)](https://codecov.io/gh/NOWUM/EnSysMod/branch/main)
[![GitHub license](https://img.shields.io/github/license/NOWUM/EnSysMod.svg)](https://github.com/NOWUM/EnSysMod/blob/main/LICENSE)
[![GitHub release](https://img.shields.io/github/release/NOWUM/EnSysMod.svg)](https://github.com/NOWUM/EnSysMod/releases/)

Just another energy system modeling tool made by Institut NOWUM-Energy - FH Aachen.

This project provides a REST API for modeling an energy system. 
It allows you to store multiple datasets in a database and generate multiple simulations from each dataset.

Unfortunately, there is no frontend yet. Feel free to contribute! ... or use [Postman](https://www.postman.com/) 
instead.

## Installation
### Using Docker
Requirements:
- [Docker](https://docs.docker.com/get-docker/)

Download Docker container from GitHub container registry:
```bash
# Latest release
docker pull ghcr.io/nowum/ensysmod:latest

# or latest development build (experts only)
docker pull ghcr.io/nowum/ensysmod:main
```

Spin up a container:
```bash
# Latest release
docker run -d -p 8080:8080 --name ensysmod ghcr.io/nowum/ensysmod:latest

# or latest development build (experts only)
docker run -d -p 8080:8080 --name ensysmod-dev ghcr.io/nowum/ensysmod:main
```

Start using the REST API by visiting http://localhost:8080/docs/

### Self-contained (experts only)
Requirements:
- [Git](https://git-scm.com/downloads)
- [Python 3.6+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/)

Clone this repository:
```bash
git clone https://github.com/NOWUM/EnSysMod.git
cd EnSysMod
```

Install requirements using conda:
```bash
# First time installation
conda env create -f requirements.yml -n EnSysMod-env

# Update conda environment
conda activate EnSysMod-env
conda env update --file requirements.yml --prune
```

Run the server:
```bash
conda activate EnSysMod-env
sh scripts/run.sh
```

Start using the REST API by visiting http://localhost:8080/docs/

## Usage
No user interface for now, sorry!

You might use Postman to consume the API.

## Contributing
Contributors are always welcome! 
For more information check out our [Contributing Guidelines](https://github.com/NOWUM/EnSysMod/blob/main/CONTRIBUTING.md). 
