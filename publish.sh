#!/bin/bash

#clean
rm -rf build/
rm -rf dist/

./make-readme.sh

python3.7 setup.py sdist bdist_wheel

#python3.6 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
python3.7 -m twine upload dist/*

