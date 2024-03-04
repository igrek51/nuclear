import dataclasses
from datetime import date, datetime
import json
from pathlib import PosixPath

import yaml


def to_json(obj) -> str:
    obj = to_json_serializable(obj)
    obj = remove_none(obj)
    return json.dumps(obj)


def to_yaml(obj) -> str:
    obj = to_json_serializable(obj)
    obj = remove_none(obj)
    return yaml.dump(obj, sort_keys=False)


def remove_none(obj):
    """Remove unwanted null values"""
    if isinstance(obj, list):
        return [remove_none(x) for x in obj if x is not None]
    elif isinstance(obj, dict):
        return {k: remove_none(v) for k, v in obj.items() if k is not None and v is not None}
    else:
        return obj


def to_json_serializable(obj):
    if dataclasses.is_dataclass(obj):
        return to_json_serializable(dataclasses.asdict(obj))
    elif isinstance(obj, PosixPath):
        return str(obj)
    elif isinstance(obj, (date, datetime)):
        return obj.isoformat()
    elif isinstance(obj, list):
        return [to_json_serializable(x) for x in obj]
    elif isinstance(obj, dict):
        return {k: to_json_serializable(v) for k, v in obj.items()}
    elif hasattr(obj, '__to_json__'):
        return getattr(obj, '__to_json__')()
    else:
        return obj
