#!/bin/bash
set -euo pipefail

MODULE_NAME=cliglue
PYTHON_INTERPRETER="${PYTHON_INTERPRETER:-python3}"

TEST_PATH="${1:-tests/}"

${PYTHON_INTERPRETER} -m coverage run --source ${MODULE_NAME} -m pytest -vv --tb=short -ra ${TEST_PATH}
# show code coverage info
${PYTHON_INTERPRETER} -m coverage report -m
