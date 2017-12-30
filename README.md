# glue.py
Common Utilities Toolkit for command line Python applications compatible with Python 2.7 and 3

## Features:
* Command Line Arguments processor: binding flags, params, commands, options
* Autogenerating help output
* Tools to keep compatibility with Python 2.7 and 3
* Logger helpers (coloured loglevels)
* Shell commands executing
* Easy string operations: splitting, splitting to tuples
* RegEx helpers: matching, filtering, replacing, extracting data
* File operations helpers
* Time to string (and vice-versa) convertions
* Collections streaming helpers: filtering, mapping

## Sample application using glue
#### sampleApp.py:
```python
#!/usr/bin/python
from glue import *

# ----- Commands and options
def commandHello(argsProcessor):
	print('Hello %s' % argsProcessor.pollNextRequired('name'))

# ----- Main
def main():
	argsProcessor = ArgsProcessor('SampleApp', '1.0.1') # app name and version
	# bind commandHello with 'hello' keyword 
	argsProcessor.bindCommand(commandHello, 'hello', description='display hello message', syntaxSuffix='<name>')
	argsProcessor.processAll() # do the magic

if __name__ == '__main__': # for testing purposes
	main() # this will not be invoked when importing this file
```
#### testing:
```$ ./sampleApp.py```, ```$ ./sampleApp.py -h``` or ```$ ./sampleApp.py --help``` will output:
```
SampleApp v1.0.1

Usage:
  ./sampleApp.py [options] <command>

Commands:
  hello <name>  - display hello message

Options:
  -h, --help    - display this help and exit
  -v, --version - print version
```

```shell
$ ./sampleApp.py hello dupa
Hello dupa
```

## Installation
Copy ```glue.py``` to your project folder.
You will need also some packages used by glue:
### Python 2.7 packages
```shell
# pip2 install future
```
for testing (optional):
```shell
# pip2 install pytest
# pip2 install coverage
# pip2 install mock
```
### Python 3 packages
```shell
# pip3 install future
```
for testing (optional):
```shell
# pip3 install pytest
# pip3 install coverage
# pip3 install mock
```