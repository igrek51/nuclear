#!/usr/bin/python
# -*- coding: utf-8 -*-
from glue import *

# ----- Actions
def actionHello(argsProcessor):
	print('Hello %s' % argsProcessor.pollNextRequired('name'))
	if argsProcessor.isFlag('force'):
		print('May the Force be with you!')

# ----- Main
def main():
	argsProcessor = ArgsProcessor('SampleApp', '1.0.1') # app name and version
	# bind actionHello with 'hello' keyword 
	argsProcessor.bindCommand(actionHello, 'hello', syntaxSuffix='<name>', description='display hello message')
	argsProcessor.bindFlag('force', syntax=['-f', '--force'], description='enable force mode')
	argsProcessor.processAll() # do the magic

if __name__ == '__main__': # for testing purposes
	main() # will not be invoked when importing this file
