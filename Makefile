.PHONY: setup test clean

PYTHON_INTERPRETER ?= python3
OUTPUT_README = README.md

setup:
	python3 -m venv venv &&\
	. venv/bin/activate &&\
	pip install --upgrade pip setuptools &&\
	pip install -r requirements.txt -r requirements-dev.txt &&\
	python setup.py develop

test:
	$(PYTHON_INTERPRETER) -m coverage run --source nuclear -m pytest -vv --tb=short -ra --color=yes $(test)
	# show code coverage info
	$(PYTHON_INTERPRETER) -m coverage report --show-missing --skip-empty --skip-covered

readme:
	cat docs/about.md > $(OUTPUT_README)

	cat docs/demo.md >> $(OUTPUT_README)
	cat docs/toc.md >> $(OUTPUT_README)
	cat docs/how-it-works.md >> $(OUTPUT_README)
	cat docs/quick-start.md >> $(OUTPUT_README)
	cat docs/vs-argparse-short.md >> $(OUTPUT_README)
	cat docs/installation.md >> $(OUTPUT_README)
	cat docs/sublog.md >> $(OUTPUT_README)
	cat docs/cheatsheet-short.md >> $(OUTPUT_README)

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf ./*.egg-info

release-pypi: clean readme
	python3 setup.py sdist bdist_wheel
	python3 -m twine upload dist/*

mkdocs-local:
	mkdocs serve

mkdocs-push:
	mkdocs gh-deploy --force


nuclear-inspect-dump:
	python3 nuclear/inspection/insta/dump.py nuclear/inspection/inspection.py
