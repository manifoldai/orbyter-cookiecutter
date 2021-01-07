# -*- coding: utf-8 -*-
"""
This module is for the evaluation of model performance.

Examples:
    Example command line executable::

        $ python evaluate.py config.yml
"""
import logging
import os

import click
import mlflow
import numpy as np

from {{cookiecutter.package_name}}.util.config import parse_config
from {{cookiecutter.package_name}}.util.logging import setup_logging_env

logger = logging.getLogger(__name__)


@click.command()
@click.argument(
    "config_file", type=click.Path(exists=True), default="/mnt/configs/config.yml"
)
@setup_logging_env
def main(config_file="config.yml"):
    """
    Main function that loads config, sets up logging, and runs evaluation

    Args:
        config_file (str): path to config file (for logging)

    Returns:
        None
    """
    logger.info("Evaluating")
    # load config
    logger.info(f"Loading config {config_file}")
    config = parse_config(config_file)
    logger.info(f"Config: \n{config}")
    # log experiment
    params = {"param0": np.random.rand()}
    metrics = {"metric0": np.random.rand()}
    artifacts = {"config_file": config_file}
    log_experiment(
        params,
        metrics,
        artifacts,
        config["experiment_name"],
        os.environ["MLFLOW_TRACKING_URI"],
        os.environ["MLFLOW_ARTIFACT_LOCATION"],
    )


def log_experiment(
    params={},
    metrics={},
    artifacts={},
    experiment_name="my_experiment",
    mlflow_tracking_uri="./experiments",
    mlflow_artifact_location=None,
):
    """
    Evaluate the model and log it with mlflow

    Args:
        params (dict): dictionary of parameters to log
        metrics (dict): dictionary of metrics to log
        artifacts (dict): dictionary of artifacts (path) to log
        experiment_name (str): experiment name
        mlflow_tracking_uri (str): path or sql url for mlflow logging
        mlflow_artifact_location (str): path or s3bucket url for artifact
            logging. If none, it will default to a standard.

    Returns:
        None
    """
    # Try to create an experiment if it doesn't exist
    try:
        exp_0 = mlflow.create_experiment(
            experiment_name, artifact_location=mlflow_artifact_location
        )
        # set uri
        mlflow.set_tracking_uri(mlflow_tracking_uri)
        logger.info(f"Created new experiment id: {exp_0}")
    except Exception as E:
        logger.info(f"{E}. Writing to same URI/artifact store")
    # Always set the experiment
    mlflow.set_experiment(experiment_name)
    logger.info(f"Running experiment {experiment_name}")
    with mlflow.start_run():
        # param logging
        for key, val in params.items():
            logger.info(f"Logging param {key}")
            mlflow.log_param(key, val)
        # metric logging
        for key, val in metrics.items():
            logger.info(f"Logging metric {key}")
            mlflow.log_metric(key, val)
        # artifact logging
        for key, val in artifacts.items():
            logger.info(f"Logging artifact {key}")
            mlflow.log_artifact(val)


if __name__ == "__main__":
    main()
