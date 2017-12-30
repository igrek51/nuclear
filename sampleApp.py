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
