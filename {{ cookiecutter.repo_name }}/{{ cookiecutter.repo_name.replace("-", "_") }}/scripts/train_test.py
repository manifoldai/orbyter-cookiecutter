import pytest
from click.testing import CliRunner

from {{cookiecutter.repo_name.replace("-", "_")}}.scripts.train import main


@pytest.mark.parametrize("config_file", [("configs/config.yml")])
def test_train(config_file):
    runner = CliRunner()
    result = runner.invoke(main, [config_file])
    assert result.exit_code == 0
