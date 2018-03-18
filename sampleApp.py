#!/usr/bin/env python
# -*- coding: utf-8 -*-
from glue import *

# ----- Actions
def actionHello(ap):
	print('Hello %s' % ap.pollNextRequired('name'))
	if ap.isFlag('force'):
		print('May the Force be with you!')

# ----- Main
def main():
	ap = ArgsProcessor('SampleApp', '1.0.1') # app name and version
	# bind actionHello with 'hello' keyword 
	ap.bindCommand(actionHello, 'hello', syntaxSuffix='<name>', description='display hello message')
	ap.bindFlag('force', syntax=['-f', '--force'], description='enable force mode')
	ap.processAll() # do the magic

if __name__ == '__main__': # for testing purposes
	main() # will not be invoked when importing this file
