#!/bin/bash

#clean
rm -rf build/
rm -rf dist/

python3.6 setup.py sdist bdist_wheel

#python3.6 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
python3.6 -m twine upload dist/*

