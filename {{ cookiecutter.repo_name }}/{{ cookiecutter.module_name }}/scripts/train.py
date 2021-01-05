# -*- coding: utf-8 -*-
"""
This module is for training models.

Examples:
    Example command line executable::

        $ python train.py config.yml
"""
import logging

import click

<<<<<<< HEAD:{{ cookiecutter.repo_name }}/{{ cookiecutter.module_name }}/scripts/train.py
from {{cookiecutter.module_name}}.util.config import parse_config
from {{cookiecutter.module_name}}.util.logging import setup_logging_env
=======
from {{cookiecutter.repo_name.lower().replace(" ", "_").replace("-", "_")}}.util.config import parse_config
from {{cookiecutter.repo_name.lower().replace(" ", "_").replace("-", "_")}}.util.logging import setup_logging_env
>>>>>>> origin/mws/fix-repo-reference:{{ cookiecutter.repo_name }}/{{ cookiecutter.repo_name.lower().replace(" ", "_").replace("-", "_") }}/scripts/train.py

logger = logging.getLogger(__name__)


@click.command()
@click.argument(
    "config_file", type=click.Path(exists=True), default="/mnt/configs/config.yml"
)
@setup_logging_env
def main(config_file="config.yml"):
    """
    Main function that loads config, sets up logging, and runs training

    Args:
        config_file (str): path to config file (for logging)

    Returns:
        None
    """
    logger.info("Training")
    logger.info(f"Loading config {config_file}")
    config = parse_config(config_file)
    logger.info(f"Config: \n{config}")


if __name__ == "__main__":
    main()
