from click.testing import CliRunner

from {{cookiecutter.package_name}}.scripts.predict import main


def test_predict():
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code == 0
