# Project Set-up

## Setting up Version Control

We recommend setting up a remote for Git version control after running `cookiecutter`.  For example, if you want to use GitHub, go to [GitHub](https://github.com/), create the repo, and push your local work.

## Setting up Continuous Integration

You can read more about continuous integration and delivery [here](https://martinfowler.com/bliki/ContinuousDelivery.html). In its default configuration, we use CI to lint and test code that gets pushed to origin. This is crucial for making sure code is always up to standards. As it currently stands this cookiecutter sets up a CircleCI configuration in the `.circleci` folder.  In future releases we will add other CI options like GitHub actions, Jenkins, etc.  To fully setup CircleCI, after running `cookiecutter` log into log into [circleCI](https://circleci.com/). Click 'Add Projects', select your project, click 'Start Building'.

## MLFlow

You have the option to set up your MLFlow configuration in the cookiecutter questions. These can always be changed later in
the .env. In the prompts, you can set MLflow's tracking URI and MLFlow's artifact location. The prompts for MLFlow in the cookiecutter are:

```
mlflow_uri [/mnt/experiments]:

mlflow_artifact []:
```

`mlflow_uri` sets the URI location. This sets where parameters, metrics, and other [run](run) details are stored. This can be local (default to /mnt/experiments) or a SQL database. The `mlflow_artifact` sets the artifact locations. Artifacts are various files, and they can be stored either on the local filesysm or a cloud storage like S3.  Note that there is additional setup required to use a cloud like AWS -- both S3 bucket setup, RDS setup, and AWS credential management. 

## <a name="setup"></a> Setting up a project
1. Install Docker: 
    - For Mac: https://store.docker.com/editions/community/docker-ce-desktop-mac
    - For Windows: https://store.docker.com/editions/community/docker-ce-desktop-windows
    - For Linux: Go to this page and choose the appropriate install for your Linux distro: https://www.docker.com/community-edition
        - Install Docker Compose (https://docs.docker.com/compose/install/#install-compose):
            ```bash
            $ sudo curl -L https://github.com/docker/compose/releases/download/1.21.0/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
            ```
            ```bash
            $ sudo chmod +x /usr/local/bin/docker-compose
            ```
            Test the installation:
            ```bash
            $ docker-compose --version
            docker-compose version 1.21.0, build 1719ceb
            ```
2. Install Python Cookiecutter package: http://cookiecutter.readthedocs.org/en/latest/installation.html >= 1.4.0
    ``` bash
    $ pip install cookiecutter
    ```
    It is recommended to set up a central virtualenv or condaenv for cookiecutter and any other "system" wide Python packages you may need.
3. Run the cookiecutter docker data science template to scaffold your new project:
   
   Using HTTPS:
   
    ``` bash
    $ cookiecutter https://github.com/manifoldai/manifold-cookiecutter-data-science.git
    ```
    
    or SSH:
    
    ``` bash
    $ cookiecutter git@github.com:manifoldai/manifold-cookiecutter-data-science.git
    ```
4. Answer all of the cookiecutter prompts for project name, description, license, etc.
5. Run the start script from the level of your new project directory:
    ``` bash
    $ ./scripts/start.sh
    ```
6. After the project image builds check which host port is being forwarded to the Jupyter notebook server inside the running container:
    ``` bash
    $ docker ps 
    ```
7. Using any browser access your notebook at localhost:{port}
8. Start working!


## Helpful Resources 
- [Docker command cheatsheet](https://www.docker.com/sites/default/files/Docker_CheatSheet_08.09.2016_0.pdf)
- [Dockerfile reference](https://docs.docker.com/engine/reference/builder/)
- [Docker Compose reference](https://docs.docker.com/compose/compose-file/)
- [Kitematic (GUI interface to work with Docker. Highly recommended if you are new to Docker!)](https://kitematic.com/)

## Contributing
PRs and feature requests very welcome!
