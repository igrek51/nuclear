from typing import Dict, Any

from .keyword import format_var_name


class InternalVars(object):
    def __init__(self):
        self.vars: Dict[str, Any] = {}

    def __getitem__(self, key):
        return self.vars[format_var_name(key)]

    def __setitem__(self, key, item):
        self.vars[format_var_name(key)] = item
