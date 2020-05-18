.PHONY: help, ci-black, ci-flake8, ci-test, isort, black, sphinx

PROJECT={{ cookiecutter.repo_name }}
CONTAINER_NAME="{{ cookiecutter.repo_name }}_bash_${USER}"  ## Ensure this is the same name as in docker-compose.yml file
VERSION_FILE:=VERSION
TAG:=$(shell cat ${VERSION_FILE})

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

git-tag:  ## Tag in git, then push tag up to origin
	git tag $(TAG)
	git push origin $(TAG)

ci-black: ## Test for black requirements
	docker exec $(CONTAINER_NAME) black --check /mnt/{{ cookiecutter.repo_name.replace("-", "_") }}

ci-flake8: ## Test for flake8 requirements
	docker exec $(CONTAINER_NAME) flake8 /mnt/{{ cookiecutter.repo_name.replace("-", "_") }}

ci-test:  ## Test unittests
	docker exec $(CONTAINER_NAME) pytest /mnt/{{ cookiecutter.repo_name.replace("-", "_") }}

ci: ci-black ci-flake8 ci-test ## Check black, flake8, and unittests
	@echo "CI sucessful"

isort: ## Runs isort, which sorts imports
	docker exec $(CONTAINER_NAME) isort -rc /mnt/{{ cookiecutter.repo_name.replace("-", "_") }}

black: ## Run black, which formats code
	docker exec $(CONTAINER_NAME) black /mnt/{{ cookiecutter.repo_name.replace("-", "_") }}

lint: isort black ## Lint repo; runs black and isort on all files
	@echo "Linting complete"

dev-start: ## Primary make command for devs, spins up containers
	@echo "Building new images from compose"
	docker-compose -f docker/docker-compose.yml --project-name $(PROJECT) up -d --build

dev-stop: ## Spins down active containers
	docker kill $(CONTAINER_NAME)
	docker kill "{{ cookiecutter.repo_name }}_mlflow_${USER}"
	docker kill "{{ cookiecutter.repo_name }}_jupyter_${USER}"

sphinx: ## Creates docs
	docker exec -e GRANT_SUDO=yes $(CONTAINER_NAME) bash -c "cd docs; make html"
