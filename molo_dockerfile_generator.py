from configobj import ConfigObj
from dockerfile_class import DockerfileClass

key_repo_url = 'repo-url'
key_container_ports = 'container-ports'
key_app_name = 'app-name'
key_app_wsgi = 'app-wsgi'


def main():
    config = ConfigObj('config.ini')
    docker = DockerfileClass()
    docker.base_image('python:2.7.10') \
        .apt_install('redis-server') \
        .run_command("git clone {} ./deploy".format(config[key_repo_url])) \
        .run_command('virtualenv ./deploy/ve') \
        .run_command('. ./deploy/ve/bin/activate') \
        .run_command('pip install gunicorn') \
        .run_command('pip install supervisor') \
        .run_command('pip install --no-cache-dir -e ./deploy/') \
        .run_command('./deploy/manage.py migrate') \
        .copy_command('db.sqlite3', './deploy/') \
        .add_command('docker-entrypoint.sh', './deploy/') \
        .run_command('chmod +x ./deploy/docker-entrypoint.sh') \
        .expose_command(config[key_container_ports]) \
        .entrypoint('./deploy/docker-entrypoint.sh', config[key_app_name], config[key_app_wsgi],
                    config[key_container_ports][0]) \
        .write()


if __name__ == "__main__":
    main()
