from click.testing import CliRunner

from {{cookiecutter.repo_name.replace("-", "_")}}.scripts.predict import main


def test_predict():
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code == 0
