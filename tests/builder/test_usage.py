from cliglue import *
from cliglue.types.filesystem import *
from tests.parser.actions import *


def test_multilevel_commands_usage():
    CliBuilder('multiapp', version='1.2.3', with_defaults=False).has(
        subcommand('git').has(
            subcommand('help', run=action_print, help='shows help'),
            subcommand('push', run=action_print).has(
                argument('remote'),
                argument('branch', required=False),
            ),
            subcommand('describe', run=action_print).has(
                flag('--tags', help='show tags'),
            ),
            subcommand('checkout', run=action_print).has(
                argument('branch', choices=list_devices, type=str),
                flag('force', '-f'),
            ),
            parameter('--work-tree', type=existing_directory, default='.'),
            parameter('--config-file', type=existing_file),
            parameter('--count', type=int),
            primary_option('-c', run=action_print).has(
                argument('key-value'),
            ),
        ),
        subcommand('nmcli').has(
            subcommand('device').has(
                subcommand('wifi'),
                argument('device_name', choices=list_devices),
            ),
        ),
        subcommand('xrandr').has(
            parameter('output', required=True, choices=['HDMI', 'eDP1']),
            flag('--primary'),
            default_action(action_print),
        ),
        subcommand('docker').has(
            subcommand('exec', run=action_print).has(
                flag('--it'),
                parameter('-u', name='user'),
                arguments(name='cmd', joined_with=' '),
            ),
            primary_option('--help', '-h', run=action_print),
        ),
        primary_option('--help', '-h', run=action_print),
    ).run()
