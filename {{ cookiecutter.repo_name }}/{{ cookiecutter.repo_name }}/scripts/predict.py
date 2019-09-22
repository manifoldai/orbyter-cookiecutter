# -*- coding: utf-8 -*-
"""
This module is for running predictions.

Examples:
    Example command line executable::

        $ python predict.py
"""
import logging

import click

from {{cookiecutter.repo_name}}.util.logging import setup_logging

logger = logging.getLogger(__name__)


@click.command()
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
    # set-up logging only once
    setup_logging()
    main()
