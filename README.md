# glue.py
Common Utilities Toolkit compatible with Python 2.7 and 3

## Features:
* Command Line Arguments processing: binding flags, params, commands, options; autogenerating help output
* Compatibility with Python 2.7 and 3
* Loggers helpers
* shell commands executing
* Easy string operations: splitting, splitting to tuples
* RegEx helpers: matching, filtering, replacing, extracting data
* File operations helpers
* Time to string (and vice-versa) convertions
* Collections streaming helpers: filtering, mapping

## Sample application using glue
```
#!/usr/bin/python
from glue import *

# ----- Commands and options
def commandSample(argsProcessor):
	print(argsProcessor.pollNextRequired('param'))

# ----- Main
def main():
	argsProcessor = ArgsProcessor('SampleApp', '1.0.1')

	argsProcessor.bindCommand(commandSample, 'sample', description='description', syntaxSuffix='<param>')
	
	argsProcessor.processAll()

if __name__ == '__main__': # for testing purposes
	main() # this will not be invoked when importing this file
```

## Installation
Copy ```glue.py``` to your project folder
### tools for Python 2.7
```
pip2 install future
```
for testing (optional):
```
pip2 install pytest
pip2 install coverage
pip2 install mock
```
### tools for Python 3
```
pip3 install future
```
for testing (optional):
```
pip3 install pytest
pip3 install coverage
pip3 install mock
```