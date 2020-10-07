"""game.py"""
from pathlib import Path
from invoke import task

FLASK = "flask"
BABEL = "pybabel"


@task(help={})
def run(ctx):
    """Run the flask application"""
    ctx.run(f"{FLASK} run")


@task(help={})
def shell(ctx):
    """Run the flask shell"""
    ctx.run(f"{FLASK} shell")


BABEL_CFG = Path("babel.cfg")
EXTRACT_OPTS = "-k _l"
POT_FILE = Path("messages.pot")
TRANSLATIONS_DIR = Path("app", "translations")


@task(
    help={
        "extract": "Extract all texts to the .pot file",
        "generate": "Generate a language translation. Set the language to translate to.",
        "update": "Update language translations.",
        "comp": "Compile translations.",
        "show": "Show commands but do not run.",
    }
)
def babel(ctx, extract=False, show=False, generate=None, comp=None, update=False):
    """Run babel commands to create translations"""
    lst_cmds = []
    if extract:
        lst_cmds.append(f"{BABEL} extract -F {BABEL_CFG} {EXTRACT_OPTS} -o {POT_FILE} .")
    if generate:
        lst_cmds.append(f"{BABEL} init -i {POT_FILE} -d {TRANSLATIONS_DIR} -l {generate}")
    if update:
        lst_cmds.append(f"{BABEL} update -i {POT_FILE} -d {TRANSLATIONS_DIR}")
    if comp:
        lst_cmds.append(f"{BABEL} compile -d {TRANSLATIONS_DIR}")

    for n, cmd in enumerate(lst_cmds):
        print(f"{cmd}")
        if not show:
            ctx.run(cmd)
