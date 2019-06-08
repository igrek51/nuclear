#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glue


# ----- Actions -----
def action_hello(ap):
    """
    Displays hello message with user name
    :param ap: ArgsProcessor - You can get the parameter values,
    flags states or any other CLI argument from here
    """
    name = ap.poll_next('name')  # get first arg from args queue
    if ap.is_param('surname'):  # optional param 'surname'
        name += ' ' + ap.get_param('surname')  # get param 'value'
    print('Hello %s' % name)
    if ap.is_flag_set('force'):  # check flag is set
        print('May the Force be with you!')


def action_list_screens():
    glue.info('Available screens: %s' % ', '.join(list_xrandr_screens()))


def action_primary_screen(ap):
    screen_name = ap.poll_next('screen')
    glue.shell('xrandr --output %s --primary' % screen_name)
    glue.info('%s set as primary' % screen_name)


def list_xrandr_screens():
    xrandr = glue.shell_output('xrandr 2>/dev/null')
    lines = glue.nonempty_lines(xrandr)
    lines = glue.regex_filter_list(lines, r'^([a-zA-Z0-9\-]+) connected')
    return glue.regex_replace_list(lines, r'^([a-zA-Z0-9\-]+) connected(.*)', '\\1')


# ----- CLI definitions -----
def main():
    # app name and version for help printing
    ap = glue.ArgsProcessor(app_name='Sample glue application', version='1.0.1')
    # bind 'hello' keyword with action_hello function
    ap.add_subcommand('hello', action=action_hello, syntax='<name>', help='display hello message')
    # enable param 'surname' (bind to '--surname <surname>' or '--surname=<surname>' syntax)
    ap.add_param('surname', help='set custom surname', choices=['brian', 'janusz', 'brianusz'])
    # bind 'force' flag to keywords '-f' or '--force'
    ap.add_flag('force', keywords=['-f', '--force'], help='enable force mode')

    # multilevel subcommands
    ap_screen = ap.add_subcommand('screen')
    ap_screen.add_subcommand('list', action=action_list_screens, help='list available screens')
    ap_screen.add_subcommand('primary', syntax='<screen>', action=action_primary_screen,
                             choices=list_xrandr_screens, help='set primary screen')

    # do the magic
    ap.process()


if __name__ == '__main__':
    main()  # it will not be invoked when importing this module for testing purposes
