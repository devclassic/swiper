from invoke import task


@task
def build(ctx):
    cmd = "uv run pyinstaller -F -w -i logo.ico main.py"
    ctx.run(cmd)
