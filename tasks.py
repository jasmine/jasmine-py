from invoke import run, task


@task
def install(context):
    run('pip install -r requirements.txt')
    run('pip install -r requirements_dev.txt')


@task
def test(context):
    run('py.test')
