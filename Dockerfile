ARG PYTHON_IMAGE=3.10-slim

FROM python:${PYTHON_IMAGE}

ARG POETRY_VERSION

LABEL org.opencontainers.image.authors="biggates2010@gmail.com"

ENV PATH=/root/.local/bin:$PATH

RUN --mount=type=bind,source=install.py,target=/install.py set -eux; \
    apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libssl-dev \
        libffi-dev \
        cargo \
        pkg-config \
    ; \
    POETRY_VERSION=$POETRY_VERSION python /install.py ; \
    apt-get purge -y \
        build-essential \
        libssl-dev \
        libffi-dev \
        cargo \
        pkg-config \
    ; \
    apt-get autoremove -y ; \
    rm -rf /var/lib/apt/lists/* ; \
    poetry --version

CMD ["python3"]