# poetry-docker

a Docker image that includes [Poetry](https://python-poetry.org/) and [Python](https://www.python.org/) for use in CI/CD pipelines.

## supported python tags

see [python_versions.json](./python_versions.json)

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
