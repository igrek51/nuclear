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
	ap.bindCommand(actionHello, 'hello', suffix='<name>', help='display hello message')
	# bind 'force' flag to keywords '-f' or '--force'
	ap.bindFlag('force', keyword=['-f', '--force'], help='enable force mode')
	# bind 'force' flag to keywords '-f' or '--force'
	ap.bindParam('name', help='set custom name')
	# do the magic
	ap.processAll()

if __name__ == '__main__':
	main() # will not be invoked when importing this module for testing purposes
