#!/usr/bin/env python3

# This scripts generates shields.io markdown text, which is used in README.md

import json


def _tag_to_markdown(tag):
    return f"![{tag} badge](https://img.shields.io/docker/v/biggates/poetry/{tag}?label=biggates%2Fpoetry&logo=docker)"


if __name__ == "__main__":
    with open("versions.json", "r") as f:
        versions = json.load(f)

        latest_poetry_tag = versions.get("poetry")[0]
        python_tags = versions.get("python")

        all_tags = []
        for python_tag in python_tags:
            all_tags.append(f"{latest_poetry_tag}-py{python_tag}")

        all_images = " ".join([_tag_to_markdown(tag) for tag in all_tags])

        all_markdown = (
            all_images
            + " [![Docker Publish Badge](https://github.com/biggates/poetry-docker/actions/workflows/docker-publish.yml/badge.svg?branch=master)](https://github.com/biggates/poetry-docker/actions/workflows/docker-publish.yml)"
        )

        all_supported_tags = "\n".join([f"- `{tag}`" for tag in all_tags])

        print("")
        print("## Tags")
        print(all_markdown)

        print("")
        print("## Supported tags")
        print(all_supported_tags)
