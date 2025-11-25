## Installation

Install package from [PyPI repository](https://pypi.org/project/nuclear) using pip:
```shell
python3 -m pip install --upgrade nuclear
```

You need Python 3.9 or newer.

## Install package in develop mode
You can install package in develop mode in order to make any changes for your own:
```bash
python -m pip install -r requirements.txt
python -m pip install -e .
```

## Testing
Running tests:
```bash
make venv
. venv/bin/activate
make test
```
