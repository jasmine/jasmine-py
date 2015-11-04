from invoke import run, task


@task
def install():
    run('pip install -r requirements.txt')
    run('pip install -r requirements_dev.txt')


@task
def test():
    run('py.test')
