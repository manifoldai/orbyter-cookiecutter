# -*- coding: utf-8 -*-
"""
This module is for logging utility functions.
"""
import logging.config
import os

import coloredlogs
import yaml
from pytictoc import TicToc
from datetime import timedelta


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


def setup_logging_env(main: Callable)-> Callable:
    def wrapper(*arg, **kwargs):
        setup_logging_env()
        load_env(find_env())
        logger.info(f"Starting func() in {sys.argv[0]}")
        t = TicToc()
        t.tic()
        main(*args, **kwargs)
        logger.info(f"Finished func() in Run time {timedelta(seconds=t.tocvalue()}")
    return wrapper
