# Session: Python Package & Dependency Management with uv

## Overview

uv is a fast Python package manager and dependency manager developed by Astral.  
It is designed as a modern, drop-in replacement for tools like pip, pip-tools, and virtualenv, with a strong focus on speed, reproducibility, and simplicity.

Key goals of uv:

- Extremely fast dependency resolution and installation
- Easy to share environments across OS platforms (e.g., between windows and linux)
- Unified workflow for environments and dependencies
- Native support for pyproject.toml
- Compatible with existing Python packaging standards

---

## Installation

### Install via the official installer (recommended)

On macOS and Linux:
    $ curl -LsSf https://astral.sh/uv/install.sh | sh    
or
    $ wget -qO- https://astral.sh/uv/install.sh | sh    

On windows (powershell, or cmd with admin rights):
    $ powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"    

Alternative installation with pipx

```
pip install pipx
pipx install uv
```

Verify installation:
uv --version

### Create project and pyproject.toml

For a new project run:

```
uv init 
```

It creates a pyproject.toml file which is a standard configuration file for python projects.
It is used to define project metadata (e.g. project name, authors, python version), package dependencies, and configurations for development tools (e.g. for linters and formaters such as for Ruff or Black) in a single, structured file. The tomlfile provides a tool-agnostic way to describe how a Python project is built and managed.
In addition, it enables reproducible installations across environments and OS systems
A bt outdated alternatives to pyproject.toml are, for example, setup.py, setup.cfg, and requirements.txt.

### Migrate from an existing environment to uv

If you work an exisitng project and want to migrate your packages and dependencies (e.g. from requirements.txt) to uv

```
uv add -r requirements.txt
```

### Create a virtual environment (without pyproject.toml)

Create .venv directory (with pyproject.toml)

```
uv venv  
```

# Creating and Managing Virtual Environments

Activate venv

* macOS / Linux: source .venv/bin/activate # TODO check if for mac same commands are used as for linux
* Windows: .venv\\Scripts\\activate


Install first package(s)

```
uv add requests numpy pytest ruff
```

Remove package

```
uv remove requests
```

The uv.lock file contains all installations and dependencies (dont change anything here). Locking is the process of resolving the dependencies in a project into a lockfile, while syncing is actually installation process, i.e. it installs the packages from the lockfile into the project environment

```
uv lock
uv snyc 
```

Run uv lock before uv snyc when you want to ensure that you’re using the correct version of each dependency (e.g. avoid any changes in the dependencies)

## Show all packages and dependencies

uv pip list

## Close envrioment

```
$ deactivate
```

## Notes

* Modify only the pyproject.toml file and then run uv lock, uv sync , but never modify the uv.lock by making changes manually (it might beak your env)

## Troubleshooting

In the case, a package cant be resolved during uv add:

1. If you have a prebuilt wheel-file for the respective package e.g. on GitHub, then use this wheel file for installation. Example uv add https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/download/v0.4.12/flash_attn-2.8.3+cu124torch2.6-cp313-cp313-linux_x86_64.whl
2. Try uv cache clean and try to downgrade the package version if possible (e.g. uv add/pip install 'package==version'). Alternatively try uv pip install <package>. However, mixed installations between uv add and uv pip install should be avoided (due that later other package installations might cause errors).
3. If this not helps, delete uv.lock and the .venv . Recreate an empty environment and install the package(s) that caused the issue first via uv addor uv pip install. Then add remaining packages