"""Python module name validation."""
import logging
import re

logging.basicConfig()
logger = logging.getLogger(__name__)


def validate_python_module_name():
    """Check that the module name given by the user is an acceptable format."""
    module_name = "{{ cookiecutter.module_name }}"
    # The following regex will only match valid Python module names
    if not re.match(r"^[_a-zA-Z][_a-zA-Z0-9]+$", module_name):
        # Warn the user, but allow for override
        logger.warning(
            "{module_name} is not a valid Python module name!\n See "
            "https://www.python.org/dev/peps/pep-0008/#package-and-module-names "
            "for naming standards.\n"
        )


if __name__ == "__main__":
    validate_python_module_name()
