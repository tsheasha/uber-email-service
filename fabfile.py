from fabric.api import local, settings, abort, run
from fabric.contrib.console import confirm

# prepare for deployment

def test():
    with settings(warn_only=True):
        result = local("nosetests -sv")
    if result.failed and not confirm("Tests failed. Continue?"):
        abort("Aborted at user request.")

def prepare():
    test()

# deploy to heroku

def pull():
    local("git pull origin master")

def heroku():
    local("git push heroku master")

def heroku_test():
    local("heroku run python tests/test_email_service.py -v && heroku run python tests/test_api.py -v")

def deploy():
    pull()
    test()
    heroku()
    heroku_test()

# rollback
def rollback():
    local("heroku rollback")
