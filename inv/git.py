"""git.py"""
from enum import Enum
from invoke import task
from pathlib import Path


class GitStatus(Enum):
    MODIFIED = 0
    STAGED = 1


class GitFile:
    def __init__(self, name, status):
        self.name = name
        self.status = status


GIT = "git"


@task()
def git(ctx):
    """Interactive git. Supports simpe add, diff, restore, status and commit."""
    temp_file = Path("t.tmp")
    while True:
        with open(temp_file, "w") as fp:
            ctx.run(f"{GIT} status -s", out_stream=fp)
        lines = open(temp_file).readlines()
        if temp_file.exists():
            temp_file.unlink()
        lines = [line.replace("\n", "") for line in lines]
        modified = []
        for line in lines:
            if line[:2] == " M":
                modified.append(GitFile(line[2:], GitStatus.MODIFIED))
            elif line[:2] == "M ":
                modified.append(GitFile(line[2:], GitStatus.STAGED))

        if not modified:
            print("No modified files")
            return
        print(f"\nModified files : {len(modified)}")
        for n, gf in enumerate(modified):
            print(f" {n} - {gf.name} - {gf.status.name}")
        cmd = input("Command [s]tatus [d]iff [a]dd [r]estore [u]nstage<index> [c]ommit e[x]it : ")
        if cmd == "x":
            break
        lst = cmd.split(" ")
        while lst:
            oper = lst.pop(0)
            print(f"oper:{oper}")
            op = oper[0]
            if op in "drau":
                # if * then do operation on all files
                if oper[1] == "*":
                    lst_opers = [x for x, _ in enumerate(modified)]
                else:
                    lst_opers = [int(oper[1:])]
                for index in lst_opers:
                    # print(f'op:{op} index:{index}')
                    gf = modified[index]
                    if op == "d":
                        ctx.run(f"{GIT} diff {gf.name}", pty=True)
                    elif op == "r":
                        ctx.run(f"{GIT} checkout -- {gf.name}", pty=True)
                    elif op == "a":
                        ctx.run(f"{GIT} add {gf.name}", pty=True)
                    elif op == "u":
                        ctx.run(f"{GIT} restore --staged {gf.name}", pty=True)
                    else:
                        print("Unknown file operation")
            elif op == "c":
                commit_message = input("Enter commit message or --amend : ")
                if commit_message:
                    if commit_message == "--amend":
                        ctx.run(f"{GIT} commit --amend", pty=True)
                    else:
                        ctx.run(f'{GIT} commit -m "{commit_message}"', pty=True)
            elif op == "s":
                ctx.run(f"{GIT} status", pty=True)
            else:
                print("Unknown operation")


PY_FILES = [
    Path("*.py"),
    Path("app", "*.py"),
    Path("app", "errors", "*.py"),
    Path("tests", "*.py"),
    Path("inv", "*.py"),
    # Path("migrations", "*.py"),
    # Path("migrations", "versions", "*.py"),
]

BLACK = "black"
BLACK_OPTS = "-l 120"
FLAKE = "flake8"
FLAKE_IGNORES = ["E501", "E203", "W503"]  # Line too long  # Whitespace before ':'  # line break before binary operator
FLAKE_OPTS = f"--ignore={','.join(FLAKE_IGNORES)}"


@task()
def black(ctx):
    """Run bloack to format python code"""
    files = " ".join([str(pa) for pa in PY_FILES])
    ctx.run(f"{BLACK} {BLACK_OPTS} {files}")


@task()
def flake(ctx):
    """Run flake8 on python code"""
    files = " ".join([str(pa) for pa in PY_FILES])
    ctx.run(f"{FLAKE} {FLAKE_OPTS} {files}")


@task(black, flake)
def clean(ctx):
    """Clean all python code using tools."""
    pass
