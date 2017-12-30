#!/usr/bin/python
from glue import *

# ----- Commands and options
def commandSample(argsProcessor):
	print(argsProcessor.pollNextRequired('param'))

# ----- Main
def start():
	argsProcessor = ArgsProcessor('SampleApp', '1.0.1')

	argsProcessor.bindCommand(commandSample, 'sample', description='description', syntaxSuffix='<param>')
	
	argsProcessor.processAll()

if __name__ == '__main__': # for testing purposes
	start()
