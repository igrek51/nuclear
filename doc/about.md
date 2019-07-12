# cliglue - glue for CLI
[![Build Status](https://travis-ci.org/igrek51/cliglue.svg?branch=master)](https://travis-ci.org/igrek51/cliglue)
[![PyPI version](https://badge.fury.io/py/cliglue.png)](https://badge.fury.io/py/cliglue)

`cliglue` is a declarative parser for command line interfaces in Python.
It's a binding glue between CLI shell arguments and functions being invoked.

`cliglue` parses and validates command line arguments provided by user when running console application.
Then it automatically triggers matched action, based on the declared Command-Line Interface rules, injecting all needed parameters.
You don't need to write the "glue" code for binding & parsing parameters every time.
So it makes writing console aplications faster and simpler.

