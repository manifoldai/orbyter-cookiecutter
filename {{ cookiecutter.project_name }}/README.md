# {{cookiecutter.project_name}}

[Put CI Badge Here]

**Note that this is a stub README that contains boilerplate for many of the common operations done inside an ML repo. You should customize it appropriately for your specific project**

{{cookiecutter.description}}

# Setup

## Basics

Clone the code to your machine using the standard Git clone command. If you have SSH keys setup the command is:

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

This builds images using the Dockerfile in docker/Dockerfile, and runs containers named after the project directory. To see the running containers, run
`docker ps`

You should see three containers running. For example, on my laptop this looks like the below. On your machine the container ids and the names of the images and running containers will be different, i.e. they will have your username rather that sdey. In addition, the local ports will be different as well. That is expected.

```bash
CONTAINER ID        IMAGE                          COMMAND                  CREATED             STATUS              PORTS                       NAMES
f168e19b8b67        {{cookiecutter.package_name}}_mlflow            "bash -c 'mlflow ui …"   4 days ago          Up 3 days           127.0.0.1:32770->5000/tcp   {{cookiecutter.package_name}}_mlflow_<username>
87f03baf686e        {{cookiecutter.package_name}}_bash     "/bin/bash"              4 days ago          Up 4 days           127.0.0.1:32768->8501/tcp   {{cookiecutter.package_name}}_bash_<username>
d9bd01600486        {{cookiecutter.package_name}}_jupyter   "bash -c 'cd /mnt &&…"   4 days ago          Up 3 days           127.0.0.1:32769->8888/tcp   {{cookiecutter.package_name}}_jupyter_<username>
```

We have also provided a simple make command to help you easily stop the containers associated with the project:

```bash
make dev-stop
```

## Makefile

We use `make` to run most of the typical developer operations, e.g. `make dev-start`, etc. For a full list of make commands, run:

```bash
make help
```

The `make` commands supported out of the box are:

```
black                          Runs black auto-linter
ci-black                       Test lint compliance using black. Config in pyproject.toml file
ci-test                        Runs unit tests using pytest
ci                             Check black, flake8, and run unit tests
dev-start                      Primary make command for devs, spins up containers
dev-stop                       Spin down active containers
docs                           Build docs using Sphinx and copy to docs folder (this makes it easy to publish to gh-pages)
git-tag                        Tag in git, then push tag up to origin
isort                          Runs isort to sorts imports
lint                           Lints repo; runs black and isort on all files
```

## Using the Containers

The docker-compose is setup to mount the working directory of the repository into each of the containers. That means that all change you make in the git repository will automatically show up in the containers, and vice versa.

The typical workflow is to do all text editing and git commands in the local host, but _run_ all the code inside the container -- either in the bash executor or the Jupyter notebook. As mentioned earlier, the containers are the _runtime_ -- they have a consistent operating system (Ubuntu), drivers, libraries, and dependencies. It ensures that the runtime is consistent across all developers and compute environments -- from your local laptop to the cloud. This is the purpose of containerization. If you would like to read more about benefits of containerization read [here](https://dzone.com/articles/5-key-benefits-docker-ci).

Let's go over each of the three containers and how to use them.

### Bash Executor

This is the container that you should go into to run experiments, e.g. etl, training, evaluation, prediction. Use the command below to go into the container from the command line:

```bash
docker exec -it <bash-executor-container-name> /bin/bash
```

In the example above, that command would be:

```bash
docker exec -it {{cookiecutter.package_name}}_bash-executer_<username> /bin/bash
```

### Jupyter Server

This is the container that you should browse to in your web browser to access Jupyter notebooks. You should go to the local port that the Jupyter server is mapped to access the standard Jupyter notebook UI, e.g. `http://localhost:<jupyter_port>`. You can look up that port using the `docker ps` command. In the example above, the user should browse to `http://localhost:32769` to see the UI.

### MLFlow Server

We are using MLFlow to log all of our experiments. You can read more about MLFlow and it's benefits on their [website](https://mlflow.org/). Similar to the Jupyter notebook, you should go to the port that the MLFlow server is mapped to access the MLFlow UI, e.g.`http://localhost:<mlflow_port>`. You can look up that port using the `docker ps` command. In the example above, the user should browse to `http://localhost:32770` to see the UI.

# Experimentation Workflow

In this section we will go over the most common usage pattern in this repo -- running an ML experiment -- which includes training a model and evaluating it's performance. Let's walk through an example step by step.

## Step 1: Get the Data

The first thing is to get the data in the right place. This sounds easy, but it is a common source of error.

Download the data and copy it to the right place. Typically we put raw data in `data/raw/` and ETLed data in `data/processed/`

## Step 2: Create a Configuration File

We have designed the code so that all experimentation is controlled by configuration files. You don't need to edit source code to run experiments. This is by design.

There are a number of example configuration files checked into the repo [here](configs/examples). Note that the configuration files only encode _deltas_ from a base config file which is located [here](configs/config.yml). The typical workflow is to construct a configuration file by hand or using some special config generation helper utilities located [here]({{cookiecutter.package_name}}/util/config.py).

You can read about the configuration file structure [here](configs/README.md). In the following we will work with the configuration file example `config_example.yml` located [here](configs/examples/config_example.yml).

## Step 3: ETL the data

Once you have the data in the right place and a configuration file, the next step is to prepare your data for training. We do this by invoking the etl script:

```bash
python {{cookiecutter.package_name}}/scripts/etl.py configs/examples/config_example.yml
```

Note that this command should be run inside the bash executor container, not on your local host. While running this command you will see info logging to the screen that tells you what the code is doing and how it is splitting the data.

```bash
>>>> put example output here <<<<
```

## Step 4: Train and Evaluate a Model

The most common script run in this repository is the `evaluate.py` script. It trains and evaluates a model. We run this script as follows:

```bash
python {{cookiecutter.package_name}}/scripts/evaluate.py configs/examples/config_example.yml
```

By default, this script will retrain a model from scratch, but you can point it do use an already trained model. We'll cover that later in the README. For now, lets assume that we are training a model from scratch. When you run the script, you will see output like the following below:

```bash
>>>> put example output here <<<<
```

The log shows what loss is being used, the model architecture, and many more things. All of these things are configurable from the config file. It's good practice to check that what is being run is what you expect. A common failure mode is human error in the configuration files leading to you to not run the experiment you expected.

After training, the code runs a number of evaluation metrics and plots and logs these all to MLFlow. If you go to MLFlow after an evaluate run, you can see all the parameters, metrics, and artifacts logged for that run. As a best practice, you should only look at the models and figures that are persisted inside MLFlow. That is the source of truth and our experiment bookkeeping. During the evaluation phase the logging should look like:

```bash
>>>> put example output here <<<<
```

## Step 5: View Run in MLFlow

Once you have run an experiment, you want to look at the results in MLFlow. The easiest way is to use the MLFlow web UI. If you open up the MLFlow UI on your browser at `http://localhost:<mlflow_port>` you should see the MLFlow UI like below.
![mlflow](docs/imgs/mlflow.png?raw=true "MLFlow UI")

The experiments are on the left. Experiments are a MLFlow construct to group together a number of related "runs" -- which are specific runs of our `evaluate.py` script. The experiment name is set through the configuration file. For example, if we're doing a set of runs around sample size, we could group them all under an experiment called `sample_size`. Under each experiment is each run -- which is given a unique name. If you click on a run of interest you can view the details of a specific run.

We log three things in a run: parameters, metrics, and artifacts. We go into each of them in more detail below.

### Parameters

These are the configuration parameters for a specific run, like model name, loss, batch size, etc. We log most of the important ones, but not everything.

If you want the detailed information about the run you should look at the `config.yml` artifact for that run. That contains all of the information about that run.

### Metrics

These are top level summary metrics that tell you how the run performed. Most of them, unless otherwise noted, are computed on the test set. Typically, there is one number we like to look `mse` -- the mean squared error between the actual and prediction. This is our error metric of interest. Lower `mse` is better.

### Artifacts

These are the file artifacts associated with a run. These include the logs, config file, and most importantly the error analysis figures. There are a number of interesting figures to look at. Note that the error analysis is typically always done on the test set, i.e. data that the model has never seen.

![mlflow](docs/imgs/mlflow_detail.png?raw=true "MLFlow Detail UI")

## Documentation

The repo created is automatically setup with Sphinx to build HTML documentation. If you write your pydoc in Google Style format, the parser will automatically generate the documentation. See [Google Style Python Docstrings](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) for examples of such docstrings.

You can build the documentation by using the appropriate make command:

```
make docs
```

The built documentation can be configured in the `./docsrc` directory. The two main files of interest are the `conf.py` and `index.rst`. For more information about configuring Sphinx, please look at their [comprehensive documentation](https://www.sphinx-doc.org/en/master/).

We have a specific structure for our docs directory which builds inside `./docsrc/_build` and then copies the built documentation over to `./docs` -- which by default is under source control. This folder can be easily setup using GitHub Pages to serve up your documentation as a static site on GitHub. For more information on how to set that up, please look at the documentation on [GitHub pages](https://pages.github.com/) and this [article](https://www.docslikecode.com/articles/github-pages-python-sphinx/).

## Conclusion

This is the basic workflow! You can run this locally or on a cloud machine. When working on a cloud machine you will likely need to to ssh tunnelling, screen, and other tools to make sure you can view MLFLow and don't have issues with network pipes breaking.

# Project Structure

```
├── LICENSE
├── README.md                 <- Project README
├── configs
|   └──config.yml             <- Project configuration for python scripts
├── data                      <- Data cache folder
│   ├── external              <- Data from third party sources.
│   ├── interim               <- Intermediate data that has been transformed.
│   ├── processed             <- The final, canonical data sets for modeling.
│   └── raw                   <- The original, immutable data dump.
├── docker
│   ├── Dockerfile            <- New project Dockerfile that sources from base ML dev image
│   ├── docker-compose.yml    <- Docker Compose configuration file
│   └── requirements.txt      <- The requirements file for reproducing the analysis environment.
│                                New libraries should be added in the requirements
├── docs                      <- Built docs are copied here for easy deploy to GitHub Pages
├── docsrc                    <- Sphinx documentation folder
│   ├── index.rst             <- ReStructured text documentation config
│   ├── conf.py               <- Sphinx configuration file
│   └── Makefile              <- Sphinx Makefile
├── experiments               <- Where to store different model experiments, e.g., model pkls and analysis
├── logging.yml               <- Logging config file
├── logs                      <- Logging directory
├── notebooks                 <- Jupyter notebooks. Naming convention is a number (for ordering),
│                                the creator's initials, and a short `-` delimited description, e.g.
│                                `1.0-jqp-initial-data-exploration`.
├── pull_request_template.md  <- Pull request template for GitHub
├── pyproject.toml            <- Config file used by black
├── tox.ini                   <- tox config file with settings for flake
├── Makefile                  <- Makefile for starting and stopping containers, lint, and local CI.
├── .github/workflows/ci.yml  <- Default GitHub Actions CI setup
├── .dvc                      <- dvc repo containing config and local cache
└── {cookiecutter.package_name}}    <- Project source directory
    ├── __init__.py           <- Makes repo a Python module
    ├── features              <- Feature engineering pipeline go here
    ├── models                <- Model pipelines go here
    ├── scripts               <- Python executable scripts
    │   ├── evaluate.py       <- Evaluation script
    |   |-- train.py          <- Training script
    |   |-- predict.py        <- Prediction script
    |   |-- etl.py            <- ETL script
    ├── util                  <- Util folder
    │   ├── config.py         <- Config file utilities
    │   └── logging.py        <- Logging utility
    └── viz                   <- Visualization functions
```

---

# Developer Workflow

Continued development in this repo is straightforward. The scaffolding is meant to be extensible -- you should add your own models, loss functions, feature engineering pipelines, etc. For brevity we are not putting information about the intended development workflow in this README. Look [here](docs/develop.md) for more information about the intended development workflow for this repo.
## DVC

Orbyter uses DVC to perform data versioning on datasets and artifacts.

### Adding a Remote to DVC


DVC uses remote repositories to store versions of data and make it easy to share with a team. If you're adding a single remote or the first of multiple, include the ``--default`` in the command as shown below. DVC determines the type of remote (file location on disk, s3 bucket, etc.) based on the `remote_url` argumentsw

Run `dvc remote add --default <remote_name> <remote_url>`


### Tracking Files

1. `dvc add <path_to_file>` - track artifact in git
2. `dvc push` - push to remote repository

### Retrieving Versions of Tracked Files

1. `git checkout <branch>`
2. `dvc pull` - sync local cache with remote cache based on current git HEAD
3. `dvc checkout` - link files in local cache to appropriate location in project repo.

