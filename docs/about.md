# Nuclear - binding glue for CLI
[![GitHub version](https://badge.fury.io/gh/igrek51%2Fnuclear.svg)](https://github.com/igrek51/nuclear)
[![PyPI version](https://badge.fury.io/py/nuclear.svg)](https://pypi.org/project/nuclear)
[![Documentation Status](https://readthedocs.org/projects/nuclear-py/badge/?version=latest)](https://nuclear-py.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://app.travis-ci.com/igrek51/nuclear.svg?branch=master)](https://app.travis-ci.com/igrek51/nuclear)
[![codecov](https://codecov.io/gh/igrek51/nuclear/branch/master/graph/badge.svg)](https://codecov.io/gh/igrek51/nuclear)
[![Github Pages](https://img.shields.io/badge/github.io-ok-brightgreen)](https://igrek51.github.io/nuclear)


`nuclear` is a declarative parser for command line interfaces in Python.
It's a binding glue between CLI shell arguments and functions being invoked.
It mostly focuses on building multi level command trees.

`nuclear` parses and validates the command line arguments provided by the user when starting a console application.
It then automatically invokes the appropriate action, based on the declared Command-Line Interface rules, injecting all the necessary  parameters.
You don't need to write the "glue" code to bind & parse the parameters each time.
This makes writing console aplications simpler and clearer.

