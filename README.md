# poetry-docker

![3.8-slim badge](https://img.shields.io/docker/v/biggates/poetry/3.8-slim?label=biggates%2Fpoetry&logo=docker) ![3.9-slim badge](https://img.shields.io/docker/v/biggates/poetry/3.9-slim?label=biggates%2Fpoetry&logo=docker) ![3.10-slim badge](https://img.shields.io/docker/v/biggates/poetry/3.10-slim?label=biggates%2Fpoetry&logo=docker) ![3.11-slim badge](https://img.shields.io/docker/v/biggates/poetry/3.11-slim?label=biggates%2Fpoetry&logo=docker) [![Docker Publish Badge](https://github.com/biggates/poetry-docker/actions/workflows/docker-publish.yml/badge.svg?branch=master)](https://github.com/biggates/poetry-docker/actions/workflows/docker-publish.yml)

a Docker image that includes [Poetry](https://python-poetry.org/) and [pipx](https://pypa.github.io/pipx/) CI/CD pipelines.

## Deprecation Notice

Deprecated, please use `weastur/poetry` instead, e.g. :

- `weastur/poetry:1.5.1-python-3.10-slim`
- `weastur/poetry:1.5.1-python-3.10-alpine`
- `weastur/poetry:1.5.1-python-3.8-slim`

## Supported tags

- `3.8-slim`
- `3.9-slim`
- `3.10-slim`
- `3.11-slim`

see [python_versions.json](./python_versions.json)

## Usage

In your pipeline / actions, replace docker image from `python` to `biggates/poetry`, for example:

```dockerfile
# FROM python:3.10-slim
FROM biggates/poetry:3.10-slim
```

## build manuly

```bash
python build --all
```

or:

```bash
python build 3.10-slim
```

## push manully

```bash
python push --all
```

or:

```bash
python push 3.10-slim
```

## details

poetry is installed to `/root/.local/bin` via pipx. In case the path fails, use the following line in Dockerfile:

```dockerfile
ENV PATH="/root/.local/bin:$PATH"
```

## Usage in multistage builds

A typical usage is use poetry to install all the dependencies in one stage, and copy the whole venv to another stage and use it.

```dockerfile
# first stage
FROM biggates/poetry:3.10-slim as venv-creator

# activate poetry
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

# add poetry managed dependencies
ADD poetry.lock ./
ADD poetry.toml ./
ADD pyproject.toml ./

# let poetry create the venv
RUN poetry install

# second stage
FROM python:3.10-slim

WORKDIR /app

# add current project files
COPY . /app

# copy the previously created venv
COPY --from=venv-creator /app/.venv /app/.venv

# activate the venv
ENV PATH="/app/.venv/bin:$PATH"

# rest of your dockerfile
CMD ["python", "-m", "myscript.py"]

```

