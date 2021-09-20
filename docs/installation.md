## Installation
### Step 1. Prerequisites
- Python 3.6 or newer (`sudo apt install python3` on Debian/Ubuntu)
- pip

### Step 2. Install package using pip
Install package from [PyPI repository](https://pypi.org/project/nuclear) using pip:
```bash
pip3 install nuclear
```

### Install package in develop mode
You can install package in develop mode in order to make any changes for your own:
```bash
pip3 install -r requirements.txt
python3 setup.py develop
```

## Testing
Running tests:
```bash
make setup
. venv/bin/activate
make test
```

