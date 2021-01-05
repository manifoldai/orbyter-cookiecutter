import pytest
from click.testing import CliRunner

<<<<<<< HEAD:{{ cookiecutter.repo_name }}/{{ cookiecutter.module_name }}/scripts/train_test.py
from {{cookiecutter.module_name}}.scripts.train import main
=======
from {{cookiecutter.repo_name.lower().replace(" ", "_").replace("-", "_")}}.scripts.train import main
>>>>>>> origin/mws/fix-repo-reference:{{ cookiecutter.repo_name }}/{{ cookiecutter.repo_name.lower().replace(" ", "_").replace("-", "_") }}/scripts/train_test.py


@pytest.mark.parametrize("config_file", [("configs/config.yml")])
def test_train(config_file):
    runner = CliRunner()
    result = runner.invoke(main, [config_file])
    assert result.exit_code == 0
