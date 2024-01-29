#!/usr/bin/env python3
from nuclear import wat
from pydantic import BaseModel


class Person(BaseModel):
    name: str


if __name__ == '__main__':
    wat.short / Person(name='george')
