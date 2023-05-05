ARG PYTHON_IMAGE

FROM python:3.10-slim as download_server

RUN python -m pip download pipx --no-cache-dir --dest /tmp/

FROM python:$PYTHON_IMAGE

ENV DEBIAN_FRONTEND=nointeractive

COPY --from=download_server /tmp/*.whl /tmp/

RUN python -m pip install --no-index --find-links=/tmp/ pipx

RUN rm -rf /tmp/*.*

RUN python -m pipx install poetry

RUN python -m pipx ensurepath
