"""Python module name validation."""
import logging
import sys
import re

logging.basicConfig()
logger = logging.getLogger(__name__)


def validate_python_module_name():
    """Check that the module name given by the user is an acceptable format."""
    module_name = "{{ cookiecutter.module_name }}"
    # The following regex will only match valid Python module names
    if not re.match(r"^[a-z][_a-z0-9]+$", module_name):
        # Warn the user, but allow for override
        logger.error(
            f"{module_name} is not a valid Python module name!\n See "
            "https://www.python.org/dev/peps/pep-0008/#package-and-module-names "
            "for naming standards.\n"
        )
        sys.exit(1)


if __name__ == "__main__":
    validate_python_module_name()
