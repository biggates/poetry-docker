import itertools
import json
import subprocess
from typing import List, Tuple

import click

DOCKER_IMAGE_NAME = "biggates/poetry"


def _get_all_poetry_versions() -> List[str]:
    with open("poetry_versions.json") as fp:
        return json.load(fp)


def _get_all_python_versions() -> List[str]:
    with open("python_versions.json") as fp:
        return json.load(fp)


def _get_full_tag_name(python_version: str, poetry_version: str) -> str:
    return f"{DOCKER_IMAGE_NAME}:{poetry_version}-py{python_version}"


def _build(python_version: str, poetry_version: str, verbose: bool = False):
    full_tag_name = _get_full_tag_name(python_version, poetry_version)

    click.echo(f"building tag={click.style(full_tag_name, fg='green')}")

    args = [
        "docker",
        "build",
        "--file",
        "Dockerfile",
        "--build-arg",
        f"PYTHON_IMAGE={python_version}",
        "--build-arg",
        f"POETRY_VERSION={poetry_version}",
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


def _push(python_version: str, poetry_version: str, verbose: bool = False):
    full_tag_name = _get_full_tag_name(python_version, poetry_version)
    click.echo(f"pushing tag={click.style(full_tag_name, fg='green')}")

    args = [
        "docker",
        "push",
        full_tag_name,
    ]

    if verbose:
        click.echo(f"will run: {click.style(' '.join(args), fg='yellow')}")

    completed_process = subprocess.run(args)

    if completed_process.returncode == 0:
        click.echo(f"Successfully pushed tag {click.style(full_tag_name, fg='green')}")
    else:
        click.echo(
            f"docker returned {click.style(completed_process.returncode, fg='red')} when pushing tag {click.style(full_tag_name, fg='red')}"
        )


@click.group
def main():
    pass


def _check_input(
    python: List[str], poetry: List[str], all: bool
) -> Tuple[List[str], List[str]]:
    _all_python_tags = _get_all_python_versions()
    if all:
        python_tags = _all_python_tags
    else:
        if isinstance(python, str):
            python = [python]
        # 选出仅在 _all_python_tags 中的 python_tags
        python_tags = set(_all_python_tags).intersection(python)
        # 打印日志以便排查问题
        ignored_tags = set(python_tags).difference(_all_python_tags)
        if len(ignored_tags) > 0:
            for ignored_tag in ignored_tags:
                click.echo(
                    f"will ignore python {click.style(ignored_tag, fg='yellow')}, which is not in whitelist"
                )

    if len(python_tags) == 0:
        click.secho("No python version specified", fg="red")

    _all_poetry_versions = _get_all_poetry_versions()
    if all:
        poetry_versions = _all_poetry_versions
    else:
        if isinstance(poetry, str):
            poetry = [poetry]
        # 选出仅在 _all_poetry_versions 中的 poetry_versions
        poetry_versions = set(_all_poetry_versions).intersection(poetry)
        # 打印日志以便排查问题
        ignored_tags = set(poetry_versions).difference(poetry_versions)
        if len(ignored_tags) > 0:
            for ignored_tag in ignored_tags:
                click.echo(
                    f"will ignore poetry {click.style(ignored_tag, fg='yellow')}, which is not in whitelist"
                )

    if len(poetry_versions) == 0:
        click.secho("No poetry version specified", fg="red")

    return (python_tags, poetry_versions)


@main.command
@click.option("--all", type=bool, required=False, default=False, is_flag=True)
@click.option(
    "--python",
    type=click.Choice(_get_all_python_versions()),
    multiple=True,
    required=False,
)
@click.option(
    "--poetry",
    type=click.Choice(_get_all_poetry_versions()),
    multiple=True,
    required=False,
)
@click.option("--verbose", type=bool, required=False, default=False, is_flag=True)
def build(python: List[str], poetry: List[str], all: bool, verbose: bool = False):
    python_tags, poetry_versions = _check_input(python, poetry, all)

    for py, poe in itertools.product(python_tags, poetry_versions):
        _build(py, poe, verbose=verbose)


@main.command
@click.option("--all", type=bool, required=False, default=False, is_flag=True)
@click.option(
    "--python",
    type=click.Choice(_get_all_python_versions()),
    multiple=True,
    required=False,
)
@click.option(
    "--poetry",
    type=click.Choice(_get_all_poetry_versions()),
    multiple=True,
    required=False,
)
@click.option("--verbose", type=bool, required=False, default=False, is_flag=True)
def push(python: List[str], poetry: List[str], all: bool, verbose: bool = False):
    python_tags, poetry_versions = _check_input(python, poetry, all)

    for py, poe in itertools.product(python_tags, poetry_versions):
        _push(py, poe, verbose=verbose)


if __name__ == "__main__":
    main()
