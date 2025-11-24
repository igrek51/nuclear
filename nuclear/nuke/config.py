import dataclasses
from datetime import datetime, timezone
from dateutil import parser as dt_parser
from pathlib import Path
from typing import Any, Type, TypeVar, Union, get_origin, get_args
import types

import yaml

from nuclear import logger

T = TypeVar('T')


def load_config(clazz: Type[T]) -> T:
    path = Path('.config.yaml')
    if not path.is_file():
        return clazz()

    try:
        with path.open() as file:
            config_dict: dict[str, Any] = yaml.load(file, Loader=yaml.FullLoader)
            config = load_config_from_dict(clazz, config_dict)
            logger.info(f'local config loaded from {path}: {config_dict}')
            return config
    except Exception as e:
        raise RuntimeError('loading local config failed') from e


def load_config_from_dict(clazz: Type[T], config_dict: dict[str, Any]) -> T:
    return _apply_overrides(clazz(), clazz, config_dict)


def _apply_overrides(obj: T, clazz: Type[T], overrides: dict[str, Any]) -> T:
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

    # automatic type conversion
    if type(obj) is str and clazz is datetime:
        return dt_parser.parse(obj).replace(tzinfo=timezone.utc)
    
    if dataclasses.is_dataclass(clazz):
        assert isinstance(obj, dict), f'expected dict type to parse into a dataclass, got {type(obj)}'
        field_types = {field.name: field.type for field in dataclasses.fields(clazz)}
        dataclass_kwargs = dict()
        for key, value in obj.items():
            if key not in field_types:
                raise KeyError(f'unexpected field "{key}" provided to type {clazz}')
            dataclass_kwargs[key] = parse_typed_object(value, field_types[key])
        return clazz(**dataclass_kwargs)
    
    elif get_origin(clazz) in {Union, types.UnionType}:  # Union or Optional type
        union_types = get_args(clazz)
        left_types = []
        for union_type in union_types:
            if dataclasses.is_dataclass(union_type):
                if obj is not None:
                    return parse_typed_object(obj, union_type)
            elif union_type is types.NoneType:
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
