# glue.py
Common Utilities Toolkit for command line Python applications compatible with Python 2.7 and 3.
glue is a library for quick developing simple command-line Python applications.

## Features:
* Command Line Arguments processor: binding commands, options, flags, params
* Autogenerating help output
* Tools for keeping compatibility with Python 2.7 and 3
* Terminal logger helpers (coloured loglevel messages)
* Shell commands executing
* Easy string operations: splitting, splitting to tuples
* RegEx helpers: matching, filtering, replacing, extracting data
* Basic file operations helpers
* Datetime to string (and vice-versa) convertions
* Collections stream helpers: filtering, mapping

## Sample application using glue
#### sampleApp.py:
```python
#!/usr/bin/python
from glue import *

# ----- Commands and options
def commandHello(argsProcessor):
	print('Hello %s' % argsProcessor.pollNextRequired('name'))
	if argsProcessor.isFlag('force'):
		print('May the Force be with you!')

# ----- Main
def main():
	argsProcessor = ArgsProcessor('SampleApp', '1.0.1') # app name and version
	# bind commandHello with 'hello' keyword 
	argsProcessor.bindCommand(commandHello, 'hello', syntaxSuffix='<name>', description='display hello message')
	argsProcessor.bindFlag('force', syntax=['-f', '--force'], description='enable force mode')
	argsProcessor.processAll() # do the magic

if __name__ == '__main__': # for testing purposes
	main() # this will not be invoked when importing this file
```
#### autogenerating help output:
```./sampleApp.py```, ```./sampleApp.py -h``` or ```./sampleApp.py --help``` will output:
```
SampleApp v1.0.1

Usage:
  ./sampleApp.py [options] <command>

Commands:
  hello <name>  - display hello message

Options:
  -h, --help    - display this help and exit
  -v, --version - print version
  -f, --force   - enable force mode
```
#### command invoking:
```shell
$ ./sampleApp.py hello dupa
Hello dupa
$ ./sampleApp.py hello dupa --force
Hello dupa
May the Force be with you!
```

## Installation
Copy ```glue.py``` to your project folder.
You will need also some packages used by glue:
### install Python 2.7 packages
```shell
# pip2 install future
```
for testing (optional but it's useful):
```shell
# pip2 install pytest
# pip2 install coverage
# pip2 install mock
```
### install Python 3 packages
```shell
# pip3 install future
```
for testing (optional but it's useful):
```shell
# pip3 install pytest
# pip3 install coverage
# pip3 install mock
```
