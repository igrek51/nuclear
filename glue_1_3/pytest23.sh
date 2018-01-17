#!/bin/bash
MODULE_NAME=glue

echo 'pytest + coverage: Python 2...'
python2 -m coverage run --source ${MODULE_NAME} -m pytest -v || exit 1
echo 'pytest + coverage: Python 3...'
python3 -m coverage run --source ${MODULE_NAME} -m pytest -v || exit 1
# show code coverage info
coverage report -m