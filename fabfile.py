from fabric.api import env, run, cd
import time

env.hosts = ["wololo@wololo.appjango.com"]
env.key_filename = "~/.ssh/id_rsa.pub"
env.forward_agent = True


def deploy():
    with cd("~/wololo-tournaments-api"):
        run("git pull")
        run("docker-compose -f production.yml down")
        # waiting for the release of RAM
        time.sleep(15)
        run("docker-compose -f production.yml build")
        run("docker-compose -f production.yml up -d")
        run("docker-compose -f production.yml run --rm django python manage.py migrate")
