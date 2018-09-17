#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glue

# ----- Actions
def actionHello(ap):
    name = ap.poll_next('name')  # get next arg
    if ap.is_param('surname'):  # optional param 'surname'
        name += ' ' + ap.get_param('surname')
	print('Hello %s' % name)

    if ap.is_flag_set('force'):
		print('May the Force be with you!')

# ----- Main
def main():
	ap = glue.ArgsProcessor('SampleApp', '1.0.1') # app name and version
	# bind actionHello with 'hello' command keyword 
    ap.bind_command(actionHello, 'hello', suffix='<name>', help_info='display hello message')
	# bind 'force' flag to keywords '-f' or '--force'
    ap.bind_flag('force', keywords=['-f', '--force'], help_info='enable force mode')
	# enable param 'surname' (bind to '--surname <surname>' syntax by default)
    ap.bind_param('surname', help_info='set custom surname')
	# do the magic
    ap.process_all()

if __name__ == '__main__':
	main() # will not be invoked when importing this module for testing purposes
