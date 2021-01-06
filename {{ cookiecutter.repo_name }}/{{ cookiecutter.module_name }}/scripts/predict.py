# -*- coding: utf-8 -*-
"""
This module is for running predictions.

Examples:
    Example command line executable::

        $ python predict.py
"""
import logging

import click

from {{cookiecutter.package_name}}.util.logging import setup_logging_env

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
