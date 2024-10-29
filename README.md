# poetry-docker

[![1.8.4-py3.13-bookworm badge](https://img.shields.io/docker/v/biggates/poetry/1.8.4-py3.13-bookworm?label=biggates%2Fpoetry&logo=docker) ![1.8.4-py3.13-slim badge](https://img.shields.io/docker/v/biggates/poetry/1.8.4-py3.13-slim?label=biggates%2Fpoetry&logo=docker) ![1.8.4-py3.12-bullseye badge](https://img.shields.io/docker/v/biggates/poetry/1.8.4-py3.12-bullseye?label=biggates%2Fpoetry&logo=docker) ![1.8.4-py3.12-slim badge](https://img.shields.io/docker/v/biggates/poetry/1.8.4-py3.12-slim?label=biggates%2Fpoetry&logo=docker) ![1.8.4-py3.11-slim badge](https://img.shields.io/docker/v/biggates/poetry/1.8.4-py3.11-slim?label=biggates%2Fpoetry&logo=docker) ![1.8.4-py3.10-bullseye badge](https://img.shields.io/docker/v/biggates/poetry/1.8.4-py3.10-bullseye?label=biggates%2Fpoetry&logo=docker) ![1.8.4-py3.10-slim badge](https://img.shields.io/docker/v/biggates/poetry/1.8.4-py3.10-slim?label=biggates%2Fpoetry&logo=docker)](https://hub.docker.com/r/biggates/poetry) [![Docker Publish Badge](https://github.com/biggates/poetry-docker/actions/workflows/docker-publish.yml/badge.svg?branch=master)](https://github.com/biggates/poetry-docker/actions/workflows/docker-publish.yml)

a Docker image that includes [Poetry](https://python-poetry.org/) for CI/CD pipelines.

## Supported tags

- `1.8.4-py3.13-bookworm`
- `1.8.4-py3.13-slim`
- `1.8.4-py3.12-bullseye`
- `1.8.4-py3.12-slim`
- `1.8.4-py3.11-slim`
- `1.8.4-py3.10-bullseye`
- `1.8.4-py3.10-slim`

See [versions.json](./versions.json) for further information.

## Usage

In your pipeline / actions, replace docker image from `python` to `biggates/poetry`, for example:

```dockerfile
# FROM python:3.10-slim
FROM biggates/poetry:1.8.4-py3.10-slim
```

## details

Poetry is installed to `/root/.local/bin`. In case the path fails, use the following line in Dockerfile:

```dockerfile
ENV PATH="/root/.local/bin:$PATH"
```

## Usage in multistage builds

A typical usage is use poetry to install all the dependencies in one stage, and copy the whole venv to another stage and use it.

```dockerfile
# first stage
FROM biggates/poetry:1.8.4-py3.10-slim as venv-creator

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

# add poetry managed dependencies
ADD poetry.lock poetry.toml pyproject.toml README.md ./

# let poetry create the venv
RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install

# second stage
FROM python:3.10-slim as runtime

# activate the venv
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# copy the previously created venv
COPY --from=venv-creator ${VIRTUAL_ENV} ${VIRTUAL_ENV}

# add current project files
COPY . /app

# rest of your dockerfile
CMD ["python", "myscript.py"]
```

reference: [Blazing fast Python Docker builds with Poetry](https://medium.com/@albertazzir/blazing-fast-python-docker-builds-with-poetry-a78a66f5aed0)
