"""game.py"""
from invoke import task

FLASK = "flask"

@task(
    help={}
)
def run(ctx):
    """Run the flask application"""
    ctx.run(f"{FLASK} run")

@task(
    help={}
)
def shell(ctx):
    """Run the flask shell"""
    ctx.run(f"{FLASK} shell")
