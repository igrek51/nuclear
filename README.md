# cliglue

[![Build Status](https://travis-ci.org/igrek51/cliglue.svg?branch=master)](https://travis-ci.org/igrek51/cliglue)

**cliglue** is a declarative parser for command line arguments in Python.
It's a glue between CLI shell arguments and functions being invoked.

It parses shell arguments and automatically triggers matched action based on the defined Command-Line Interface rules.
It binds particular actions to commands and CLI parameters to injected function parameters.

First, you need to declare the tree with your CLI rules.
The rest is done automatically:
- Parsing flags, parameters, sub-commands, positional arguments,
- Invoking triggered action,
- Injecting all the required parameters to the function.

## How does it work?

## Command line parser
`glue` contains command line parser with autocompletion,
which simplifies and speeds up developing process of simple command-line applications.

You only need to bind a keyword to the function and `glue` is doing all the rest for you:
* It autogenerates `help` message screen.
* It adds standard options `--help`, `--version`, `-h`, `-v` by default.
* It parses automatically all the commands, flags and parameters.
* It provides bash autocompletion feature
(by pressing `Tab` you get the most relevant CLI arguments hints and autocompletion)
* It can be extended by your custom auto-completers for your commands
* It supports multilevel subcommands (`git` style alike syntax, i.e. `git remote set-url --add origin url`)
* It supports both parameters syntaxes: `--param value` or `--param=value`

## Features
* Command Line Arguments processor (parser): binding commands, flags, parameters
* Autogenerating help output
* Tools for keeping compatibility with Python 2.7 and 3 (input)
* Terminal logger helpers (coloured loglevel messages)
* Shell commands executing (with outputs and error codes)
* RegEx helpers: matching, filtering, replacing, extracting data, batch operations
* Easy string operations: splitting, splitting to tuples
* Basic file operations helpers
* Datetime to string (and vice-versa) convertions

## cliglue vs argparse
argparse:
- no multilevel sub-commands
- no autocompletion
- declarative way of CLI logic
- auto action binding & injecting arguments
glue:
- easier CLI building
- a new way of building and documenting Command Line Interface

## Quick start

Let's create simple command-line application using **cliglue**:

### hello.py
```python
#!/usr/bin/env python3
from cliglue import CliBuilder, argument, parameter, flag


def say_hello(name: str, reverse: bool, repeat: int):
    if reverse:
        name = name[::-1]
    print(f'Hello {name}.' * repeat)


def main():
    CliBuilder('hello-app', run=say_hello).has(
        argument('name'),
        flag('reverse'),
        parameter('repeat', type=int, default=1),
    ).run()


if __name__ == '__main__':
    main()
```

## More examples



## Library Installation
Copy `glue.py` to your project folder and add it to imports (just like in the examples shown above).
You will need to install some packages used by glue:
### Installing Python 3 packages
```shell
# apt install python3-pip # (for Debian)
# pip3 install future
```
testing modules (optional but it's useful):
```shell
# pip3 install pytest coverage mock
```


## Install package in develop mode
```bash
sudo python3 setup.py develop
```

## Requirements
- Install Python 3.6+


### Running tests
Running tests:
```bash
git clone https://github.com/igrek51/glue
cd glue
./pytest23.sh
```
