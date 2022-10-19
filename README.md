# Docker ML Cookiecutter

**Helping ML teams easily move to a Docker-first development workflow to iterate and deliver projects faster and more reliably.**

*New to Docker? Check out [this writeup](https://medium.freecodecamp.org/a-beginner-friendly-introduction-to-containers-vms-and-docker-79a9e3e119b) on containers vs virtual machines and how Docker fits in.*

*Cookiecutter is a command-line utility that automatically scaffolds new projects for you based on a template (referred to as cookiecutters)*: [Cookiecutter Documentation](https://cookiecutter.readthedocs.io/en/stable/)


This cookiecutter is used in conjunction with a base development image available in [Docker Hub](https://hub.docker.com/r/manifoldai/orbyter-ml-dev/) to provide a ready environment out-of-the-box for many Machine Learning project use cases. After running this cookiecutter and the provided start script a developer will have a local development setup that looks like this: 

![docker local dev](https://s3-us-west-1.amazonaws.com/manifold-public-no-vpn/torus_local_dev.png)

By scaffolding your data science projects using this cookiecutter you will get:

- Project Docker image built with your own Dockerfile for project specific requirements
- Docker Compose configuration that dynamically binds to a free host port and forwards to the jupyter server listening port inside the container
- Shared volume configuration for accessing and executing all your project code inside of the controlled container environment
- Ability to edit code using your favorite IDE on your host machine and seeing real-time changes to the runtime environment
- Jupyter notebook fully configured with nb-extensions ready for development and feature engineering
- Common data science and plotting libraries pre-installed in the container environment to start working immediately

There are several downstream benefits for moving to a container-first workflow in terms of model and inference engine deployment/delivery. By using containers early in the development cycle you can remove a lot of the configuration management issues that waste developer time and ultimately lower quality of deliverables.

## Why Did We Build This?


We are trying to bridge the gap that exists between data science and dev/operations teams today. We wrote [more about it here](https://www.kdnuggets.com/2018/05/torus-docker-first-data-science.html).


## Support

The Orbyter cookiecutter supports Python 3.x

# Project Set-up

## Setting up Version Control

We recommend setting up a remote for Git version control after running `cookiecutter`.  For example, if you want to use GitHub, go to [GitHub](https://github.com/), create the repo, and push your local work.


## Setting up Continuous Integration

You can read more about continuous integration and delivery [here](https://martinfowler.com/bliki/ContinuousDelivery.html). In its default configuration, we use CI to format, lint, and test code that gets shared with others. This is crucial for ensuring code is always up to standards. This cookiecutter currently sets up a Github Actions configuration in the `.github` folder.  Other CI options include Jenkins, CircleCI, etc.


## Setting up MLFlow

You have the option to configure MLFlow through the cookiecutter prompts. This configuration can be changed later in `.env`. In the prompts, you can set MLflow's tracking URI and MLFlow's artifact location. The prompts for MLFlow in the cookiecutter are:

```
mlflow_uri [/mnt/experiments]:

mlflow_artifact []:
```

`mlflow_uri` sets the URI location. This sets where parameters, metrics, and other [run](run) details are stored. This can be local (default to /mnt/experiments) or a SQL database. The `mlflow_artifact` option sets the artifact locations. Artifacts are various files, and they can be stored either on the local file system or cloud storage like S3.  Note that there is additional setup required to use a cloud provider like AWS (S3 bucket setup, RDS setup, and AWS credential management). 


## <a name="setup"></a> Setting up a project
1. Install Docker: 
    - For Mac: https://store.docker.com/editions/community/docker-ce-desktop-mac
        - It is important to select _Mac with Apple Chip_ if you have an Apple Silicon (M1, M2) chip. Check _About this Mac > Overview > Chip_ for Apple or Intel.
    - For Windows: https://store.docker.com/editions/community/docker-ce-desktop-windows
    - For Linux: Go to [this page](https://www.docker.com/community-edition) and choose the appropriate install for your Linux distro: 
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
2. Install Cookiecutter (`>= 1.4.0`) through Python. Follow the [installation guide](https://cookiecutter.readthedocs.io/en/stable/installation.html) if the following installation through `pip` fails:
    ``` bash
    $ python3 -m pip install cookiecutter
    ```
    It is recommended to set up a central virtualenv or condaenv for cookiecutter and any other "system-wide" Python packages you may need.

3. Run the cookiecutter docker data science template to scaffold your new project:
   
   Using HTTPS:
   
    ``` bash
    $ cookiecutter https://github.com/manifoldai/orbyter-cookiecutter.git
    ```
    
    or SSH:
    
    ``` bash
    $ cookiecutter git@github.com:manifoldai/orbyter-cookiecutter.git
    ```

4. Answer all of the cookiecutter prompts for project name, description, license, etc. You will have to select the base image. See [orbyter-docker project](https://github.com/manifoldai/orbyter-docker/blob/master/README.md) for descriptions of available images.

5. There are a series of commands pre-defined in `Makefile`. Run the appropriate `make` command from the level of your new project directory to build and run your Docker image:
    ``` bash
    $ make dev-start
    ```

6. After the project image builds, check which host port is being forwarded to the Jupyter notebook server inside the running container:
    ``` bash
    $ docker ps 
    ```

7. Using any browser access your notebook at localhost:{port}. You can also
    automatically open this (Note: this will only work on MAC due to open command):
    ``` bash
    $ make lab
    ```
8. Start working!


## Helpful Resources 
- [Docker command cheatsheet](https://www.docker.com/wp-content/uploads/2022/03/docker-cheat-sheet.pdf)
- [Dockerfile reference](https://docs.docker.com/engine/reference/builder/)
- [Docker Compose reference](https://docs.docker.com/compose/compose-file/)


## Contributing
PRs and feature requests very welcome!
