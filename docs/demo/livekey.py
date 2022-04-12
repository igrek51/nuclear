#!/usr/bin/env python3
import random
import time

from nuclear.sublog import log
from nuclear import shell


def key_type(text):
    text = text.replace('"', '\\"')
    for character in text:
        shell(f'xdotool key type "{character}"')
        time.sleep(random.uniform(0, 0.2))


def key_enter():
    shell('xdotool key Return')


def type_line(line: str):
    key_type(line.strip())
    time.sleep(0.5)
    key_enter()


def countdown():
    for i in range(3):
        log.info(f'Starting in {3-i}...')
        time.sleep(1)
    log.info('Action!')


def type_demo():
    commands = [
        './demo.py hello Nuclear',
        './demo.py',
        './demo.py calculate --help',
        './demo.py calculate factorial 6',
        './demo.py calculate primes 100',
        './demo.py hello --help',
        './demo.py hello --repeat 3 --decode UGlja2xl',
    ]
    for command in commands:
        type_line(command)
        time.sleep(1.5)


if __name__ == '__main__':
    countdown()
    type_demo()
    log.info('Cut!')
