# poetry-docker

![3.8-slim badge](https://img.shields.io/docker/v/biggates/poetry/3.8-slim?label=biggates%2Fpoetry&logo=docker) ![3.9-slim badge](https://img.shields.io/docker/v/biggates/poetry/3.9-slim?label=biggates%2Fpoetry&logo=docker) ![3.10-slim badge](https://img.shields.io/docker/v/biggates/poetry/3.10-slim?label=biggates%2Fpoetry&logo=docker) ![3.11-slim badge](https://img.shields.io/docker/v/biggates/poetry/3.11-slim?label=biggates%2Fpoetry&logo=docker) [![Docker Publish Badge](https://github.com/biggates/poetry-docker/actions/workflows/docker-publish.yml/badge.svg?branch=master)](https://github.com/biggates/poetry-docker/actions/workflows/docker-publish.yml)

a Docker image that includes [Poetry](https://python-poetry.org/) and [pipx](https://pypa.github.io/pipx/) CI/CD pipelines.

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
