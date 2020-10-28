# -*- coding: utf-8 -*-
"""
This module is for logging utility functions.
"""
import logging.config
import os
import sys
from datetime import timedelta
from pathlib import Path
from typing import Callable

import coloredlogs
import numpy as np
import yaml
from dotenv import find_dotenv, load_dotenv
from pytictoc import TicToc


logger = logging.getLogger(__name__)


def setup_logging(logging_config="logging.yml", default_level=logging.INFO):
    """
    Setup logging configuration

    Args:
        logging (str): logging yaml config
        default_level (logging.LEVEL): default logging level

    Returns:
        None
    """
    # from config
    if os.path.exists(logging_config):
        with open(logging_config, "rt") as f:
            config = yaml.safe_load(f)
        # make sure logging directory exists
        Path(config["handlers"]["info_file_handler"]["filename"]).parent.mkdir(
            exist_ok=True
        )
        Path(config["handlers"]["error_file_handler"]["filename"]).parent.mkdir(
            exist_ok=True
        )
        logging.config.dictConfig(config)
        config_method = logging_config
        # set colored log (console streaming) to use params set in config
        console_format = config["formatters"][
            config["handlers"]["console"]["formatter"]
        ]["format"]
        console_level = config["handlers"]["console"]["level"]
        console_stream = config["handlers"]["console"]["stream"]
        coloredlogs.install(fmt=console_format, level=console_level, sys=console_stream)
        # install color logging for all modules
        for log_name, log_dict in config["loggers"].items():
            coloredlogs.install(
                fmt=console_format,
                level=log_dict["level"],
                logger=logging.getLogger(log_name),
            )
        # and root/__main__
        coloredlogs.install(
            fmt=console_format,
            level=config["root"]["level"],
            logger=logging.getLogger("__main__"),
        )

    # from default
    else:
        logging.basicConfig(level=default_level)
        config_method = "default_level"
        coloredlogs.install(level="DEBUG")
    logger.info(f"Logging set from {config_method}")


def setup_logging_env(main: Callable) -> Callable:
    """Decorator to set up loggging and load env variables

    Args:
        main: top level function (typically main triggered by CLI)

    Return:
        function after setting up logging and loading env variables
    """

    def wrapper(*args, **kwargs):
        setup_logging()
        load_dotenv(find_dotenv())
        logger.info("Loaded environment variables")
        logger.info(f"Starting {main.__name__}() in {sys.argv[0]}")
        t = TicToc()
        t.tic()
        main(*args, **kwargs)
        logger.info(
            f"Finished {main.__name__}() in "
            f"{timedelta(seconds=np.ceil(t.tocvalue()))}"
        )

    return wrapper
