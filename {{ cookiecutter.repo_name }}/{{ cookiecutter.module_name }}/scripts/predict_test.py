from click.testing import CliRunner

<<<<<<< HEAD:{{ cookiecutter.repo_name }}/{{ cookiecutter.module_name }}/scripts/predict_test.py
from {{cookiecutter.module_name}}.scripts.predict import main
=======
from {{cookiecutter.repo_name.lower().replace(" ", "_").replace("-", "_")}}.scripts.predict import main
>>>>>>> origin/mws/fix-repo-reference:{{ cookiecutter.repo_name }}/{{ cookiecutter.repo_name.lower().replace(" ", "_").replace("-", "_") }}/scripts/predict_test.py


def test_predict():
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code == 0
