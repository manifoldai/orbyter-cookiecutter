import pytest
import pathlib

from click.testing import CliRunner

from {{cookiecutter.package_name}}.scripts.train import main, _main

_HERE = pathlib.Path(__file__).resolve().parent


@pytest.mark.parametrize("config_file", [("configs/config.yml")])
def test_click_main(config_file):
    """
    This tests the _main() click runner AND ensures the main() function within it works
    correctly when called by click

    If `result.exit_code` is non-zero, inserting the following lines right before the
    `assert` statement can be very helpful for debugging. This will turn off `black`
    formatting, then print the stack trace for the python function that failed.
    ```
    import traceback; traceback.print_exception(*result.exc_info)
    ```
    """
    runner = CliRunner()
    result = runner.invoke(_main, [config_file])
    assert result.exit_code == 0


def test_main():
    """ This tests the function main() independently from the _main() click command
    
    This pattern aids in writing tests, as the function with the click decorators can be
    separately tested from the script functionality itself. In addition, the main()
    function can now be imported and used in other python modules
    """
    config_path = _HERE.parents[1].joinpath("configs", "config.yml")
    assert main(config_path) is None
