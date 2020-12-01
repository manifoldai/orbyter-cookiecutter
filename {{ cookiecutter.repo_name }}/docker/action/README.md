# Dockerfile CI action

This action executes arbitrary commands within a Docker container defined by
the local Dockerfile. Commands are passed to the container via the `command`
input and received by an entrypoint script `action-exec.sh` that feeds the
command string to `bash -c`

## Documentation
The documentation for how this action works can be found here:
* [Creating a Docker container action](https://docs.github.com/en/free-pro-team@latest/actions/creating-actions/creating-a-docker-container-action)
* [Dockerfile support for GitHub Actions](https://docs.github.com/en/free-pro-team@latest/actions/creating-actions/dockerfile-support-for-github-actions)

## Inputs

### `command`

**Required** - String of commands and arguments to pass to `bash -c` command.
Default command is `pytest {{ cookiecutter.repo_name }}`.

## Example usage

```yaml
steps:
  - name: Checkout
    uses: actions/checkout@v1
  - name: CI
    uses: ./docker/action
    with:
      command: pytest {{ cookiecutter.repo_name }}
```
