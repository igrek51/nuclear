import dataclasses
import json
from datetime import datetime, timezone
from pathlib import Path
import sys
from typing import Any, Type, TypeVar, Union, get_origin, get_args

import yaml

from nuclear import logger, ContextError
from nuclear.nuke.invoke import parse_cli_args

T = TypeVar('T')
UnionType = type(str | None)
NoneType = type(None)


def load_config(clazz: Type[T]) -> T:
    try:
        local_overrides = _load_local_overrides()
        _, cli_overrides = parse_cli_args(sys.argv[1:])
        if cli_overrides:
            logger.debug('Applying CLI overrides to config', cli_overrides=cli_overrides)

        overrides: dict[str, Any] = local_overrides | cli_overrides
        return apply_overrides(clazz(), clazz, overrides)

    except Exception as e:
        raise ContextError('loading config failed', e)


def _load_local_overrides() -> dict[str, Any]:
    path = Path('.config.yaml')
    if not path.is_file():
        return {}

    yaml_content = path.read_text()
    yaml_dict: dict[str, Any] = yaml.safe_load(yaml_content)
    logger.info('local config loaded', config_path=path)
    return yaml_dict


def apply_overrides(obj: T, clazz: Type[T], overrides: dict[str, Any]) -> T:
    field_types: dict[str, Type] = clazz.__annotations__
    for key, value in overrides.items():
        if key not in field_types:
            raise KeyError(f'unexpected field "{key}" provided for type {clazz}')
        converted_value = parse_typed_object(value, field_types[key])
        setattr(obj, key, converted_value)
    return obj


def parse_typed_object(obj: Any, clazz: Type[T]):
    if obj is None:
        return None

    if type(obj) is str:
        if clazz is datetime:
            return datetime.fromisoformat(obj).replace(tzinfo=timezone.utc)
        elif get_origin(clazz) is list and get_args(clazz)[0] is str:
            return json.loads(obj)
        elif clazz is bool:
            return obj.lower() in {'true', 'yes', 'on', '1', 'y', 't'}
        elif clazz in [int, float]:
            return clazz(obj)
    
    if dataclasses.is_dataclass(clazz):
        assert isinstance(obj, dict), f'expected dict type to parse into a dataclass, got {type(obj)}'
        field_types = {field.name: field.type for field in dataclasses.fields(clazz)}
        dataclass_kwargs = dict()
        for key, value in obj.items():
            if key not in field_types:
                raise KeyError(f'unexpected field "{key}" provided to type {clazz}')
            dataclass_kwargs[key] = parse_typed_object(value, field_types[key])
        return clazz(**dataclass_kwargs)
    
    elif get_origin(clazz) in {Union, UnionType}:  # Union or Optional type
        union_types = get_args(clazz)
        left_types = []
        for union_type in union_types:
            if dataclasses.is_dataclass(union_type):
                if obj is not None:
                    return parse_typed_object(obj, union_type)
            elif union_type is NoneType:
                if obj is None:
                    return None
            else:
                left_types.append(union_type)
        if not left_types:
            raise ValueError(f'none of the union types "{clazz}" match to a given value: {obj}')
        if len(left_types) > 1:
            raise ValueError(f'too many ambiguous union types {left_types} ({clazz}) matching to a given value: {obj}')
        return parse_typed_object(obj, left_types[0])
    
    elif get_origin(clazz) is None and isinstance(obj, clazz):
        return obj

    else:
        try:
            return clazz(obj)
        except BaseException as e:
            raise ValueError(f'failed to parse "{obj}" ({type(obj)}) to type {clazz}: {e}')
