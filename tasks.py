"""tasks.py"""
# flake8: noqa
from invoke import task

from inv.git import git, black, flake, clean


# @task
# def test(ctx):
# """Run pytest to test code."""
# ctx.run("pytest tests/", pty=True)
