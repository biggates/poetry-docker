import json
import subprocess
from typing import List

import click

DOCKER_IMAGE_NAME = "biggates/poetry"


def _get_all_python_versions() -> List[str]:
    with open("python_versions.json", "r") as fp:
        return json.load(fp)

def _build(tag: str, verbose: bool = False):
    click.echo(
        f"building tag={click.style(tag, fg='green')}"
    )

    full_tag_name = f"{DOCKER_IMAGE_NAME}:{tag}"

    args = [
        "docker",
        "build",
        "--file",
        "Dockerfile",
        "--build-arg",
        f"PYTHON_IMAGE={tag}",
        "--tag",
        full_tag_name,
        ".",
    ]

    if verbose:
        args.append("--progress=plain")
        click.echo(f"will run: {click.style(' '.join(args), fg='yellow')}")

    completed_process = subprocess.run(args)

    if completed_process.returncode == 0:
        click.echo(f"Successfully built tag {click.style(full_tag_name, fg='green')}")
    else:
        click.echo(
            f"docker returned {click.style(completed_process.returncode, fg='red')} when building tag {click.style(full_tag_name, fg='red')}"
        )


@click.group
def main():
    pass


@main.command
@click.option("--all", type=bool, required=False, default=False, is_flag=True)
@click.argument("tags", type=click.Choice(_get_all_python_versions()), nargs=-1, required=False)
@click.option("--verbose", type=bool, required=False, default=False, is_flag=True)
def build(tags: List[str], all: bool, verbose: bool = False):
    _all_tags = _get_all_python_versions()
    if all:
        tags = _all_tags
    else:
        ignored_tags = set(tags).difference(_all_tags)
        tags = set(tags).intersection(_all_tags)
        if len(ignored_tags) > 0:
            for ignored_tag in ignored_tags:
                click.echo(
                    f"will ignore tag {click.style(ignored_tag, fg='yellow')}, which is not in whitelist"
                )

    if len(tags) == 0:
        click.secho("No tag(s) specified", fg="red")

    for tag in tags:
        _build(tag, verbose=verbose)


if __name__ == "__main__":
    main()
