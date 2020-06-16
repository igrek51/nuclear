# cliglue - glue for CLI
[![GitHub version](https://badge.fury.io/gh/igrek51%2Fcliglue.svg)](https://github.com/igrek51/cliglue)
[![PyPI version](https://badge.fury.io/py/cliglue.svg)](https://pypi.org/project/cliglue)
[![Documentation Status](https://readthedocs.org/projects/cliglue/badge/?version=latest)](https://cliglue.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://travis-ci.org/igrek51/cliglue.svg?branch=master)](https://travis-ci.org/igrek51/cliglue)
[![Coverage Status](https://coveralls.io/repos/github/igrek51/cliglue/badge.svg?branch=master)](https://coveralls.io/github/igrek51/cliglue?branch=master)
[![codecov](https://codecov.io/gh/igrek51/cliglue/branch/master/graph/badge.svg)](https://codecov.io/gh/igrek51/cliglue)


`cliglue` is a declarative parser for command line interfaces in Python.
It's a binding glue between CLI shell arguments and functions being invoked.
It mostly focuses on building multi level command trees.

`cliglue` parses and validates command line arguments provided by user when running console application.
Then it automatically triggers matched action, based on the declared Command-Line Interface rules, injecting all needed parameters.
You don't need to write the "glue" code for binding & parsing parameters every time.
So it makes writing console aplications simpler and more clear.

