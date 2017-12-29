#!/bin/bash
MODULE_NAME=glue_1_2

echo 'pytest + coverage: Python 2...'
python2 -m coverage run --source ${MODULE_NAME} -m pytest -v
echo 'pytest + coverage: Python 3...'
python3 -m coverage run --source ${MODULE_NAME} -m pytest -v

coverage report -m