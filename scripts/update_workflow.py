#!/usr/bin/env python3

# This script generates the docker publish workflow (./.github/workflows/update-versions.yml).
# This script runs ./versions.json as input.
# This script should be run from the root of the repository.

import json
from string import Template

WORKFLOW_BEFORE = """# This file is generated by scripts/update_workflow.py
name: Docker Publish
on:
  push:
    branches: [ "master" ]
  pull_request:
    branches: [ "master" ]
  workflow_dispatch:

env:
  REGISTRY: docker.io
  IMAGE_NAME: biggates/poetry

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
      # This is used to complete the identity challenge
      # with sigstore/fulcio when running outside of PRs.
      id-token: write
"""

WORKFLOW_AFTER = """
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Docker buildx
        uses: docker/setup-buildx-action@v3

      - name: Download poetry installer
        run: |
          wget -q -S -O install.py https://install.python-poetry.org

      # Login against a Docker registry except on PR
      # https://github.com/docker/login-action
      - name: Log into registry ${{ env.REGISTRY }}
        if: github.event_name != 'pull_request'
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: build and push docker image
        if: github.event_name != 'pull_request'
        uses: docker/build-push-action@v6
        with:
          context: .
          file: ./Dockerfile
          push: true
          tags: biggates/poetry:${{ matrix.poetry_version }}-py${{ matrix.python_version }}
          build-args: |
            PYTHON_IMAGE=${{ matrix.python_version }}
            POETRY_VERSION=${{ matrix.poetry_version }}
"""

WORKFLOW_MATRIX_TEMPLATE = Template("""
    strategy:
      matrix:
        python_version: $python_versions
        poetry_version: $poetry_versions
        include:
          - poetry_version: "2.0.1"
            python_version: "3.13-bookworm"
          - poetry_version: "2.0.1"
            python_version: "3.13-slim"
          - poetry_version: "1.8.5"
            python_version: "3.13-bookworm"
          - poetry_version: "1.8.5"
            python_version: "3.13-slim"

""")

if __name__ == "__main__":
    with open("versions.json", "r") as f:
        versions = json.load(f)

    new_workflow_content = (
        WORKFLOW_BEFORE
        + WORKFLOW_MATRIX_TEMPLATE.substitute(
            python_versions=json.dumps(versions["python"]),
            poetry_versions=json.dumps(versions["poetry"]),
        )
        + WORKFLOW_AFTER
    )

    output_file = ".github/workflows/docker-publish.yml"

    with open(output_file, "r") as f:
        old_workflow_content = f.read()

        if old_workflow_content == new_workflow_content:
            # skip generation if contents are equal
            exit(0)

    with open(output_file, "w") as f:
        f.write(new_workflow_content)
