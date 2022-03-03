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

Our documentation is available [here](https://nowum.github.io/EnSysMod/).

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
- [GUROBI](https://www.gurobi.com/downloads) or [GLPK](https://www.gnu.org/software/glpk/glpk.html)

Clone this repository:
```bash
git clone https://github.com/NOWUM/EnSysMod.git
cd EnSysMod
```

Install requirements:
```bash
sh scripts/install.sh
```

Run the server:
```bash
sh scripts/run.sh
```

Start using the REST API by visiting http://localhost:8080/docs/

If you want to run an optimization, you need to install a solver like [Gurobi](https://www.gurobi.com/) or [GLPK]
(https://www.gnu.org/software/glpk/glpk.html).


## Usage
No user interface for now, sorry!

You might use Postman to consume the API.

A detailed documentation is available [here](https://nowum.github.io/EnSysMod/).

## Contributing
Contributors are always welcome! 
For more information check out our [Contributing Guidelines](https://github.com/NOWUM/EnSysMod/blob/main/CONTRIBUTING.md). 
