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
