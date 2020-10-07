"""tasks.py"""
# flake8: noqa
from invoke import task

from inv.git import git, black, flake, clean
from inv.fl import run, shell, babel


@task
def test(ctx):
    """Run pytest to test code."""
    ctx.run("pytest -v tests/", pty=True)
