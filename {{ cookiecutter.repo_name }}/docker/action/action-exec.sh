#!/bin/bash
# This script is used as the entry-point for the GitHub action defined by
# action.yml. This script executes the commands and arguments passed to the
# action via the `command` key.

bash -c "$*"
