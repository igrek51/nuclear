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
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glue

# ----- Actions
def actionHello(ap):
	name = ap.pollNext('name') # get next arg
	if ap.isParam('surname'): # optional param 'surname'
		name += ' ' + ap.getParam('surname')
	print('Hello %s' % name)

	if ap.isFlag('force'):
		print('May the Force be with you!')

# ----- Main
def main():
	ap = glue.ArgsProcessor('SampleApp', '1.0.1') # app name and version
	# bind actionHello with 'hello' command keyword 
	ap.bindCommand(actionHello, 'hello', suffix='<name>', help='display hello message')
	# bind 'force' flag to keywords '-f' or '--force'
	ap.bindFlag('force', keywords=['-f', '--force'], help='enable force mode')
	# enable param 'surname' (bind to '--surname <surname>' syntax by default)
	ap.bindParam('surname', help='set custom surname')
	# do the magic
	ap.processAll()

if __name__ == '__main__':
	main() # will not be invoked when importing this module for testing purposes
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
$ python sampleApp.py hello dupa --surname myOldFriend
Hello dupa myOldFriend
```

## Installation
Copy ```glue.py``` to your project folder and add it to imports (just like in the example shown above).
You will need also some packages used by glue:
### install Python 2.7 packages
```shell
# apt install python-pip # (for Debian)
# pip2 install future
```
testing modules (optional but it's useful):
```shell
# pip2 install pytest coverage mock
```
### install Python 3 packages
```shell
# apt install python3-pip # (for Debian)
# pip3 install future
```
testing modules (optional but it's useful):
```shell
# pip3 install pytest coverage mock
```

## ToDo
* auto generating bash completion for declared commands and options
* multilevel commands - git style alike (git push origin master)
