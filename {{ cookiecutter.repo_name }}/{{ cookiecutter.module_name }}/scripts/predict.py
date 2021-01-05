# -*- coding: utf-8 -*-
"""
This module is for running predictions.

Examples:
    Example command line executable::

        $ python predict.py
"""
import logging

import click

<<<<<<< HEAD:{{ cookiecutter.repo_name }}/{{ cookiecutter.module_name }}/scripts/predict.py
from {{cookiecutter.module_name}}.util.logging import setup_logging_env
=======
from {{cookiecutter.repo_name.lower().replace(" ", "_").replace("-", "_")}}.util.logging import setup_logging_env
>>>>>>> origin/mws/fix-repo-reference:{{ cookiecutter.repo_name }}/{{ cookiecutter.repo_name.lower().replace(" ", "_").replace("-", "_") }}/scripts/predict.py

logger = logging.getLogger(__name__)


@click.command()
@setup_logging_env
def main():
    """
    Main function that loads config, sets up logging, and runs predictions

    Args:
        None

    Returns:
        None
    """
    logger.info("Predicting")


if __name__ == "__main__":
    main()
