# Setup

This document describes how to set up your environment to work with this repository.

## Get the repository

Clone the code to your machine using the standard Git clone command. If you have SSH keys set up, the command is (where you should replace `manifoldai` if working in a different org):

```bash
git clone git@github.com:manifoldai/{{cookiecutter.package_name}}.git
```

Important note: **Do not clone your code into Google Drive or DropBox**. There are known issues with MLFlow interacting with the file sync that is happening in the background. Clone to a directory that is not being synced by one of those services.

## Docker

You will need to have Docker and docker-compose installed on your system to run the code.

### Install Docker

- For Mac: https://store.docker.com/editions/community/docker-ce-desktop-mac
- For Windows: https://store.docker.com/editions/community/docker-ce-desktop-windows
- For Linux: Go to this page and choose the appropriate install for your Linux distro: https://www.docker.com/community-edition

### Install Docker Compose:

```
$ sudo curl -L https://github.com/docker/compose/releases/download/1.21.0/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
$ sudo chmod +x /usr/local/bin/docker-compose
```

Test the installation:

```
$ docker-compose --version
docker-compose version 1.21.0, build 1719ceb
```

## Start Docker Containers

The runtime for {{cookiecutter.project_name}} is inside a Docker container. We have a `make` command to launch the appropriate containers. To launch the docker containers and begin working on a CPU, run from the root directory of the repository:

```bash
make dev-start
```

This builds images using the Dockerfile in docker/Dockerfile, and runs containers named after the project directory. To see the running containers, run `docker ps`.

You should see two containers running. Note that the local ports could be different on your machine: this is to be expected.

```bash
$ docker ps
CONTAINER ID   IMAGE                  COMMAND                  CREATED         STATUS        PORTS                                                  NAMES
c5df791a2731   {{ cookiecutter.package_name }}_develop   "bash -c 'cd /mnt &&…"   3 seconds ago   Up 1 second   127.0.0.1:55003->8888/tcp                              {{ cookiecutter.package_name }}_develop_<username>
451fa5f876dc   {{ cookiecutter.package_name }}_mlflow    "bash -c 'mlflow ser…"   3 seconds ago   Up 1 second   127.0.0.1:55004->5000/tcp                              {{ cookiecutter.package_name }}_mlflow_<username>
```

Note the local addresses 127.0.0.1:55003 and 127.0.0.1:55004, which tell us where to access the Jupyterlab server and the MLFlow server respectively (see below for more details).

We have also provided `make dev-stop` and `make dev-rebuild` to stop all containers and to rebuild the containers respectively.

## Makefile

We use `make` to run most of the typical developer operations, e.g. `make dev-start`, etc. For a full list of make commands, run:

```bash
make help
```

The `make` commands supported out of the box are:

```
bash                           Provides an interactive bash shell in the container
black                          Runs black auto-linter
ci-black                       Test lint compliance using black. Config in pyproject.toml file
ci-mypy                        Runs mypy type checker
ci-test-interactive            Runs unit tests with interactive IPDB session at the first failure
ci-test                        Runs unit tests using pytest
ci                             Check black, flake8, and run unit tests
clean                          Clean out temp/compiled python files
dev-rebuild                    Rebuild images for dev containers (useful when Dockerfile/requirements are updated)
dev-start                      Primary make command for devs, spins up containers
dev-stop                       Spin down active containers
docs                           Build docs using Sphinx and copy to docs folder (this makes it easy to publish to gh-pages)
format                         Formats repo by running black and isort on all files
git-tag                        Tag in git, then push tag up to origin
ipython                        Provides an interactive ipython prompt
isort                          Runs isort to sorts imports
```

## Using the Containers

The `docker-compose.yml` file is setup to mount the working directory of the repository into each of the containers. That means that all changes you make in the git repository will automatically show up in the containers, and vice versa.

The typical workflow is to do all text editing and git commands in the local host, but _run_ all the code inside the develop container, either in a notebook or through the shell. As mentioned earlier, the containers are the _runtime_ -- they have a consistent operating system (Ubuntu), drivers, libraries, and dependencies. It ensures that the runtime is consistent across all developers and compute environments -- from your local laptop to the cloud. This is the purpose of containerization. If you would like to read more about benefits of containerization read [here](https://dzone.com/articles/5-key-benefits-docker-ci).

Let's go over the two containers and how to use them.

### Develop Container

This container will run all your code. It's running a Jupyterlab server on port 8888 of the container, which is mapped to a port on your local machine as described above.

You should also use this container to run experiments, preprocessing and any similar
tasks. We typically run these through an interactive bash session (`make bash`).

### MLFlow Server

We use MLFlow to track and log of our experiments. You can read more about MLFlow and its benefits on the [MLFlow website](https://mlflow.org/). Just like the Jupyterlab server, you can access it using the corresponding port in the output of `docker ps`.
