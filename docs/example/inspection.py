#!/usr/bin/env python3
from nuclear import inspect, wat, wats

from pydantic import BaseModel


class Person(BaseModel):
    name: str


if __name__ == '__main__':
    wats / Person(name='george')
