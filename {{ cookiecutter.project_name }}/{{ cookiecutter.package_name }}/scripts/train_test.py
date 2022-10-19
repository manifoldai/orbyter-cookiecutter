import pathlib

import pytest
from click.testing import CliRunner

from {{cookiecutter.package_name}}.scripts.train import _main, main

_HERE = pathlib.Path(__file__).resolve().parent


@pytest.mark.parametrize("config_file", [("configs/config.yml")])
def test_click_main(config_file):
    """Tests both _main() click runner and its call to main()"""
    runner = CliRunner()
    try:
        result = runner.invoke(_main, [config_file])
        assert result.exit_code == 0
    except AssertionError:
        import traceback

        traceback.print_exception(*result.exc_info)
        raise


def test_main():
    """Tests the function main() independently from main() click command

    This pattern aids in writing tests, as the function with the click decorators can be
    separately tested from the script functionality itself. In addition, the main()
    function can now be imported and used in other python modules
    """
    config_path = _HERE.parents[1].joinpath("configs", "config.yml")
    assert main(config_path) is None
