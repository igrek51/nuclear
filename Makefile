.PHONY: venv test clean build dist

PYTHON_INTERPRETER ?= python3
OUTPUT_README = README.md
SHELL = bash

venv:
	uv venv venv --python 3.12 &&\
	. venv/bin/activate &&\
	uv pip install -r requirements.txt -r requirements-dev.txt &&\
	python setup.py develop

setup-test-unit:
	python3 -m venv venv &&\
	. venv/bin/activate &&\
	pip install -r requirements.txt -r requirements-dev.txt &&\
	python -m pip install -e .

test:
	$(PYTHON_INTERPRETER) -m coverage run --source nuclear -m pytest -vv --tb=short -ra --color=yes $(test)
	# show code coverage info
	$(PYTHON_INTERPRETER) -m coverage report --show-missing --skip-empty --skip-covered

readme:
	cat docs/about.md > $(OUTPUT_README)
	echo -en '\n\n' >> $(OUTPUT_README)
	cat docs/demo.md >> $(OUTPUT_README)
	echo -en '\n\n' >> $(OUTPUT_README)
	# cat docs/toc.md >> $(OUTPUT_README)
	# echo -en '\n\n' >> $(OUTPUT_README)
	# cat docs/how-it-works.md >> $(OUTPUT_README)
	# echo -en '\n\n' >> $(OUTPUT_README)
	# cat docs/quick-start.md >> $(OUTPUT_README)
	# echo -en '\n\n' >> $(OUTPUT_README)
	# cat docs/vs-argparse-short.md >> $(OUTPUT_README)
	# echo -en '\n\n' >> $(OUTPUT_README)
	# cat docs/installation.md >> $(OUTPUT_README)
	# echo -en '\n\n' >> $(OUTPUT_README)
	# cat docs/cheatsheet-short.md >> $(OUTPUT_README)
	# echo -en '\n\n' >> $(OUTPUT_README)
	cat docs/sublog.md >> $(OUTPUT_README)
	echo -en '\n\n' >> $(OUTPUT_README)
	cat docs/shell.md >> $(OUTPUT_README)

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf ./*.egg-info

build:
	python setup.py sdist bdist_wheel

release: clean readme build
	python -m twine upload -u __token__ dist/*

mkdocs-local:
	mkdocs serve

mkdocs-push:
	mkdocs gh-deploy --force
