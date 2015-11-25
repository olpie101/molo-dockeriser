# MOLO Dockeriser
###### A Dockerfile Genrator for setting up Molo mobi sites

*Molo Dockeriser* is a tool for creating Dockerfiles used to create docker containers for sites based on [Molo](https://molo.readthedocs.org/).

The goal is to make the creation of Docker containers as easy as possible.

### Setup

__NB: The use of a virtual environment is highly recommended__
```shell
pip install -e .
```
Ensure that you have [Docker](https://www.docker.com/) already installed and you are ready to go!!!
________
The dockeriser uses a the `config.ini` configuration file to generate the correct `Dockerfile`. The config file contains the following variables:

__repo-url__ — location of the molo website repository. Providing a directory is currently not supported.

__container-ports__ — ports which should be exposed in the docker container, each port separated by a comma (ie. 8000,8080). The first specified port number will be used as for the access url.

__app-name__ — identifies the running application in the docker container

__app-wsgi__ — reference to the *wsgi* used to start the application service

The `config.ini` is already setup with an [example](https://github.com/praekelt/molo-tuneme) to help you get started.

Currently an sqlite3 database with the name `db.sqlite3` is required for the Dockerfile to be successfully created. This ensures that the db has a superuser already set up. This shall be fixed in a later updated. For now a ensure the `db.sqlite3` file is present in the root directory. __NB: make sure that the database file provided has all the necessary migrations applied or :boom:!__

### Usage

To create the Dockerfile simply execute
```bash
python ./molo_dockerfile_generator.py
```
Create the docker image using
```bash
docker build -t molo-container .
```
Run the image using
```bash
docker run -it -p 8088:8000 molo-test #for interactive shell OR
docker run -d -p 8088:8000 molo-test #run in background
```
Ensure that the port number corresponds to the first port number provided in the the config file. This creates a port forwarding from your host machine on port *8088* to port *8000* on the docker container.

To view the application running in the container navigate to `localhost:8088` in your browser. This __will not work on Mac OS X__.

For Mac OS X you need to navigate to the virtual machine's ip address. To find out what ip address to use use the following command:
```
docker-machine ls
```
This only works if you are using the more recent *Docker Toolbox* and not *Boot2Docker*. You should get an output similar to this:
```
NAME      ACTIVE   DRIVER       STATE     URL                         SWARM
default   -        virtualbox   Running   tcp://192.168.99.101:2376
```
Use the ip address which is displayed. Using the results from above, to view the application on OS X would require you to navigate to `192.168.99.101:8088`.
