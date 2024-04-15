ARG PYTHON_IMAGE=3.10-slim

FROM python:$PYTHON_IMAGE as download_server
ARG POETRY_VERSION

RUN python -m pip download pipx poetry==$POETRY_VERSION --no-cache-dir --dest /tmp/ 

FROM python:$PYTHON_IMAGE
ARG POETRY_VERSION

ENV DEBIAN_FRONTEND=nointeractive

COPY --from=download_server /tmp/*.whl /tmp/

LABEL org.opencontainers.image.authors="biggates2010@gmail.com"

RUN python -m pip install --no-index --find-links=/tmp/ pipx

RUN python -m pipx install poetry==${POETRY_VERSION} --pip-args "--no-index --find-links=/tmp/"
RUN python -m pipx ensurepath && rm -rf /tmp/*.whl
