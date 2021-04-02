from setuptools import find_packages, setup

setup(
    name="{{ cookiecutter.package_name }}",
    author="{{ cookiecutter.author_name }}",
    author_email="{{ cookiecutter.author_email }}",
    packages=find_packages(),
    install_requires=[],
    python_requires=">=3.7",
    license="{{ cookiecutter.open_source_license }}",
)
