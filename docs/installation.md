## Installation
### Step 1. Prerequisites
- Python 3.6 (or newer)
- pip
#### on Debian 10 (buster)
```bash
sudo apt install python3.7 python3-pip
```
#### on Debian 9 (stretch)
Unfortunately, Debian stretch distribution does not have Python 3.6+ in its repositories, but it can be compiled from the source:
```bash
wget https://www.python.org/ftp/python/3.6.9/Python-3.6.9.tgz
tar xvf Python-3.6.9.tgz
cd Python-3.6.9
./configure --enable-optimizations --with-ensurepip=install
make -j8
sudo make altinstall
```
#### on Ubuntu 18
```bash
sudo apt install python3.6 python3-pip
```
#### on Centos 7
```bash
sudo yum install -y python36u python36u-libs python36u-devel python36u-pip
```
#### on Fedora
```bash
sudo dnf install python36
```

### Step 2. Install package using pip
Install package from [PyPI repository](https://pypi.org/project/nuclear) using pip:
```bash
pip3 install nuclear
```
Or using explicit python version:
```bash
python3.6 -m pip install nuclear
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
pip3 install -r requirements.txt -r requirements-dev.txt
./pytest.sh
```

