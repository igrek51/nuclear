#!/bin/bash

#clean
rm -rf build/
rm -rf dist/

# increment __version__

./make-readme.sh

python3 setup.py sdist bdist_wheel

#python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
python3 -m twine upload dist/*
