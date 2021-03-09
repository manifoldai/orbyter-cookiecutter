# {{cookiecutter.project_name}}

[Put CI Badge Here]

**Note that this is a stub README that contains boilerplate for many of the common operations done inside an ML repo. You should customize it appropriately for your specific project**

{{cookiecutter.description}}

This file outlines the experimentation and development workflow. You should modify it for your project to describe any project-specific scripts, data sources, configuration parameters that are specific to your project.

For information on how to setup this project (including Docker), see [SETUP.md](SETUP.md).

## Experimentation Workflow

In this section we will go over the most common usage pattern in this repo -- running an ML experiment -- which includes training a model and evaluating its performance. Let's walk through an example step by step.

### Step 1: Get the Data

The first thing is to get the data in the right place. This sounds easy, but it is a common source of error.

Download the data and copy it to the right place. Typically we put raw data in `data/raw/` and ETLed data in `data/processed/`

### Step 2: EDA

EDA and other exploratory work typically happens in notebooks. We recommend
organizing your notebooks within the `notebooks/` directory, using a file
structure and naming convention that works for your project (e.g.,
individual-specific notebooks should be prefaced with that person's initials,
etc.). Note that the `notebooks/scratch/` subdirectory is by default not tracked
in git, which makes it a good place for one-off analyses, or as a staging area
to avoid polluting your `git status`.

### Step 3: Create a Configuration File

We have designed the code so that all experimentation is controlled by configuration files. You don't need to edit source code to run experiments. This is by design.

There are a number of example configuration files checked into the repo [here](configs/examples). Note that the configuration files only encode _deltas_ from a base config file which is located [here](configs/config.yml). The typical workflow is to construct a configuration file by hand or using some special config generation helper utilities located [here]({{cookiecutter.package_name}}/util/config.py).

You can read about the configuration file structure [here](configs/README.md). In the following we will work with the configuration file example `config_example.yml` located [here](configs/examples/config_example.yml).

### Step 4: ETL the data

Once you have the data in the right place and a configuration file, the next step is to prepare your data for training. We do this by writing and invoking an ETL script:

```bash
$ make bash
$ python {{cookiecutter.package_name}}/scripts/etl.py configs/examples/config_example.yml
```

Note that we use `make bash` to ensure that the code runs in the develop container, not on your local host.
While running this command, you should see info logging to the screen that tells you what the code is doing and how it is splitting the data.

### Step 5: Train and Evaluate a Model

The most common script run in this repository is the `evaluate.py` script. It trains and evaluates a model. We run this script as follows:

```bash
python {{cookiecutter.package_name}}/scripts/evaluate.py configs/examples/config_example.yml
```

By default, this script will retrain a model from scratch, but you can point it do use an already trained model. We'll cover that later in the README. For now, lets assume that we are training a model from scratch. When you run the script, you will see output like the following below:

The log shows what loss is being used, the model architecture, and many more things. All of these things are configurable from the config file. It's good practice to check that what is being run is what you expect. A common failure mode is human error in the configuration files leading to you to not run the experiment you expected.

After training, the code runs a number of evaluation metrics and plots and logs these all to MLFlow. If you go to MLFlow after an evaluate run, you can see all the parameters, metrics, and artifacts logged for that run. As a best practice, you should only look at the models and figures that are persisted inside MLFlow. That is the source of truth and our experiment bookkeeping. During the evaluation phase the logging should look like:

### Step 6: View Run in MLFlow

Once you have run an experiment, you want to look at the results in MLFlow. The easiest way is to use the MLFlow web UI. If you open up the MLFlow UI on your browser at `http://localhost:<mlflow_port>` you should see the MLFlow UI like below.
![mlflow](docs/imgs/mlflow.png?raw=true "MLFlow UI")

The experiments are on the left. Experiments are a MLFlow construct to group together a number of related "runs" -- which are specific runs of our `evaluate.py` script. The experiment name is set through the configuration file. For example, if we're doing a set of runs around sample size, we could group them all under an experiment called `sample_size`. Under each experiment is each run -- which is given a unique name. If you click on a run of interest you can view the details of a specific run.

We log three things in a run: parameters, metrics, and artifacts. We go into each of them in more detail below.

#### Parameters

These are the configuration parameters for a specific run, like model name, loss, batch size, etc. We log most of the important ones, but not everything.

If you want the detailed information about the run you should look at the `config.yml` artifact for that run. That contains all of the information about that run.

#### Metrics

These are top level summary metrics that tell you how the run performed. Most of them, unless otherwise noted, are computed on the test set. Typically, there is one number we like to look `mse` -- the mean squared error between the actual and prediction. This is our error metric of interest. Lower `mse` is better.

#### Artifacts

These are the file artifacts associated with a run. These include the logs, config file, and most importantly the error analysis figures. There are a number of interesting figures to look at. Note that the error analysis is typically always done on the test set, i.e. data that the model has never seen.

![mlflow](docs/imgs/mlflow_detail.png?raw=true "MLFlow Detail UI")

### Documentation

The repo created is automatically setup with Sphinx to build HTML documentation. If you write your pydoc in Google Style format, the parser will automatically generate the documentation. See [Google Style Python Docstrings](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) for examples of such docstrings.

You can build the documentation by using the appropriate make command:

```
make docs
```

The built documentation can be configured in the `./docsrc` directory. The two main files of interest are the `conf.py` and `index.rst`. For more information about configuring Sphinx, please look at their [comprehensive documentation](https://www.sphinx-doc.org/en/master/).

We have a specific structure for our docs directory which builds inside `./docsrc/_build` and then copies the built documentation over to `./docs` -- which by default is under source control. This folder can be easily setup using GitHub Pages to serve up your documentation as a static site on GitHub. For more information on how to set that up, please look at the documentation on [GitHub pages](https://pages.github.com/) and this [article](https://www.docslikecode.com/articles/github-pages-python-sphinx/).

### Conclusion

This is the basic workflow! You can run this locally or on a cloud machine. When working on a cloud machine you will likely need to to ssh tunnelling, screen, and other tools to make sure you can view MLFLow and don't have issues with network pipes breaking.

## Project Structure

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
├── notebooks                 <- Jupyter notebooks.
│   └── scratch               <- Notebooks not tracked by git
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

## Developer Workflow

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
