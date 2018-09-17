#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glue


# ----- Actions -----
def action_hello(ap):
    name = ap.poll_next('name')  # get first arg
    if ap.is_param('surname'):  # optional param 'surname'
        name += ' ' + ap.get_param('surname')
    msg = 'Hello %s' % name
    if ap.is_flag_set('force'):  # check flag is set
        msg += ', May the Force be with you!'
    print(msg)


# ----- Args definitions -----
def main():
    ap = glue.ArgsProcessor('SampleApp', '1.0.1')  # app name and version
    # bind 'hello' keyword with action_hello command
    ap.add_subcommand('hello', action=action_hello, syntax='<name>', description='display hello message')
    # bind 'force' flag to keywords '-f' or '--force'
    ap.add_flag('force', keywords=['-f', '--force'], description='enable force mode')
    # enable param 'surname' (bind to '--surname <surname>' or '--surname=<surname>' syntax by default)
    ap.add_param('surname', description='set custom surname')
    # do the magic
    ap.process()


if __name__ == '__main__':
    main()
