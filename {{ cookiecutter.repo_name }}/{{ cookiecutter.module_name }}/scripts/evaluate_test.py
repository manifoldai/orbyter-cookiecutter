import os

import pytest
from click.testing import CliRunner

<<<<<<< HEAD:{{ cookiecutter.repo_name }}/{{ cookiecutter.module_name }}/scripts/evaluate_test.py
from {{cookiecutter.module_name}}.scripts.evaluate import main
=======
from {{cookiecutter.repo_name.lower().replace(" ", "_").replace("-", "_")}}.scripts.evaluate import main
>>>>>>> origin/mws/fix-repo-reference:{{ cookiecutter.repo_name }}/{{ cookiecutter.repo_name.lower().replace(" ", "_").replace("-", "_") }}/scripts/evaluate_test.py


@pytest.mark.parametrize("config_file", [("configs/config.yml")])
def test_evaluate(config_file):
    runner = CliRunner()
    os.environ["MLFLOW_TRACKING_URI"] = "./experiments"
    os.environ["MLFLOW_ARTIFACT_LOCATION"] = ""
    result = runner.invoke(main, [config_file])
    assert result.exit_code == 0
