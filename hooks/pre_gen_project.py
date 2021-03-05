"""Python module name validation.

Compatible with python 2 and python 3, to ensure cookiecutter support
across various platforms
"""
import logging
import sys
import re

logging.basicConfig()
logger = logging.getLogger(__name__)

REF_URL = "https://www.python.org/dev/peps/pep-0008/#package-and-module-names"


def validate_python_package_name():
    """Check that the module name given by the user is an acceptable format."""
    package_name = "{{ cookiecutter.package_name }}"
    # The following regex will only match valid Python module names
    if not re.match(r"^[a-z][_a-z0-9]+$", package_name):
        # Error out if you have an invalid module name
        err = "{} is not a valid Python module name!\n See {} for naming standards."
        logger.error(err.format(package_name, REF_URL))
        sys.exit(1)


if __name__ == "__main__":
    validate_python_package_name()
