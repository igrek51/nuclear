# nuclear - binding glue for CLI
[![GitHub version](https://badge.fury.io/gh/igrek51%2Fnuclear.svg)](https://github.com/igrek51/nuclear)
[![PyPI version](https://badge.fury.io/py/nuclear.svg)](https://pypi.org/project/nuclear)
[![Documentation Status](https://readthedocs.org/projects/nuclear-py/badge/?version=latest)](https://nuclear-py.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://travis-ci.org/igrek51/nuclear.svg?branch=master)](https://travis-ci.org/igrek51/nuclear)
[![codecov](https://codecov.io/gh/igrek51/nuclear/branch/master/graph/badge.svg)](https://codecov.io/gh/igrek51/nuclear)


`nuclear` is a declarative parser for command line interfaces in Python.
It's a binding glue between CLI shell arguments and functions being invoked.
It mostly focuses on building multi level command trees.

`nuclear` parses and validates command line arguments provided by user when running console application.
Then it automatically triggers matched action, based on the declared Command-Line Interface rules, injecting all needed parameters.
You don't need to write the "glue" code for binding & parsing parameters every time.
So it makes writing console aplications simpler and more clear.

