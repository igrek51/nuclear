import random
import time

from nuclear.sublog import log
from nuclear import shell


def key_type(text, key_delay: float):
    text = text.replace('"', '\\"')
    for character in text:
        shell(f'xdotool key type "{character}"')
        time.sleep(key_delay * random.uniform(0.5, 1))


def key_enter():
    shell('xdotool key Return')


def type_line(line: str, key_delay: float):
    key_type(line.strip(), key_delay)
    time.sleep(key_delay * 3)
    key_enter()


def countdown():
    for i in range(3):
        log.info(f'Starting in {3-i}...')
        time.sleep(1)
    log.info('Action!')


def animate_commands(commands: list[str], key_delay: float = 0.2, line_delay: float = 1.5):
    countdown()
    for command in commands:
        type_line(command, key_delay)
        time.sleep(line_delay)
    log.info('Cut!')
