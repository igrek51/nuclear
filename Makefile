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

generate-readme:
		cat docs/about.md > $(OUTPUT_README)
		cat docs/demo.md >> $(OUTPUT_README)
		cat docs/features.md >> $(OUTPUT_README)
		cat docs/how-it-works.md >> $(OUTPUT_README)
		cat docs/quick-start.md >> $(OUTPUT_README)
		cat docs/vs-argparse.md >> $(OUTPUT_README)
		cat docs/installation.md >> $(OUTPUT_README)

		cat docs/builder.md >> $(OUTPUT_README)
		cat docs/subcommands.md >> $(OUTPUT_README)
		cat docs/flags.md >> $(OUTPUT_README)
		cat docs/parameters.md >> $(OUTPUT_README)
		cat docs/positional-args.md >> $(OUTPUT_README)
		cat docs/many-args.md >> $(OUTPUT_README)
		cat docs/dictionaries.md >> $(OUTPUT_README)
		cat docs/autocompletion.md >> $(OUTPUT_README)
		cat docs/help.md >> $(OUTPUT_README)
		cat docs/data-types.md >> $(OUTPUT_README)
		cat docs/errors.md >> $(OUTPUT_README)
		cat docs/sublog.md >> $(OUTPUT_README)
		cat docs/cheatsheet.md >> $(OUTPUT_README)

clean:
		rm -rf build/
		rm -rf dist/
		rm -rf ./*.egg-info

release-pypi: clean generate-readme
		python3 setup.py sdist bdist_wheel
		python3 -m twine upload dist/*
