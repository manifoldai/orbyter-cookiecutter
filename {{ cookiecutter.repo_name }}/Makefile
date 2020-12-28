.PHONY: help, ci-black, ci-flake8, ci-test, isort, black, docs

PROJECT={{ cookiecutter.repo_name }}
CONTAINER_NAME="{{ cookiecutter.repo_name }}_bash_${USER}"  ## Ensure this is the same name as in docker-compose.yml file
PROJ_DIR="/mnt/{{ cookiecutter.repo_name.replace("-", "_") }}"
VERSION_FILE:=VERSION
TAG:=$(shell cat ${VERSION_FILE})

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

git-tag:  ## Tag in git, then push tag up to origin
	git tag $(TAG)
	git push origin $(TAG)

ci-black: ## Test lint compliance using black. Config in pyproject.toml file
	docker exec $(CONTAINER_NAME) black --check $(PROJ_DIR)

ci-flake8: ## Test lint compliance using flake8. Config in tox.ini file
	docker exec $(CONTAINER_NAME) flake8 $(PROJ_DIR)

ci-test:  ## Runs unit tests using pytest
	docker exec $(CONTAINER_NAME) pytest $(PROJ_DIR)

ci-test-interactive:  ## Runs unit tests using pytest, and gives you an interactive IPDB session at the first failure
	docker exec -it $(CONTAINER_NAME) pytest $(PROJ_DIR)  -x --pdb --pdbcls=IPython.terminal.debugger:Pdb

ci: ci-black ci-flake8 ci-test ## Check black, flake8, and run unit tests
	@echo "CI sucessful"

isort: ## Runs isort to sorts imports
	docker exec $(CONTAINER_NAME) isort -rc $(PROJ_DIR)

black: ## Runs black auto-linter
	docker exec $(CONTAINER_NAME) black $(PROJ_DIR)

lint: isort black ## Lints repo; runs black and isort on all files
	@echo "Linting complete"

dev-start: ## Primary make command for devs, spins up containers
	@echo "Building new images from compose"
	docker-compose -f docker/docker-compose.yml --project-name $(PROJECT) up -d --build

dev-stop: ## Spin down active containers
	docker-compose -f docker/docker-compose.yml --project-name {{ cookiecutter.repo_name }} down


docs: ## Build docs using Sphinx and copy to docs folder (this makes it easy to publish to gh-pages)
	docker exec -e GRANT_SUDO=yes $(CONTAINER_NAME) bash -c "cd docsrc; make html"
	@cp -a docsrc/_build/html/. docs

ipython: ## Provides an interactive ipython prompt
	docker exec -it $(CONTAINER_NAME) ipython
