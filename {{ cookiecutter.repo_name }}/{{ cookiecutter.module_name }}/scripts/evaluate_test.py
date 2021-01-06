import os

import pytest
from click.testing import CliRunner

from {{cookiecutter.package_name}}.scripts.evaluate import main


@pytest.mark.parametrize("config_file", [("configs/config.yml")])
def test_evaluate(config_file):
    runner = CliRunner()
    os.environ["MLFLOW_TRACKING_URI"] = "./experiments"
    os.environ["MLFLOW_ARTIFACT_LOCATION"] = ""
    result = runner.invoke(main, [config_file])
    assert result.exit_code == 0
