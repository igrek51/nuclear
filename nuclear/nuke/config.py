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


class NukeConfig:
    """Default configuration for nuke tasks.
    
    Extend this class to add custom configuration fields:
        class Config(NukeConfig):
            limit: int = 0
            output_dir: str = 'dist'
    """
    dry: bool = False


def load_config(clazz: Type[T]) -> T:
    try:
        local_overrides = _load_local_overrides()
        cli_args = sys.argv[1:]
        _, cli_overrides = parse_cli_args(cli_args, config_class=clazz)
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
        if '.' in key:
            # Dotted key traverses nested objects: --level1.level2.param=value
            parts = key.split('.')
            current_obj = obj
            current_field_types = field_types
            for part in parts[:-1]:
                part_clean = part.replace('-', '_')
                if part_clean not in current_field_types:
                    raise KeyError(f'unexpected field "{part}" in path "{key}" for type {type(current_obj).__name__}')
                current_obj = getattr(current_obj, part_clean)
                next_clazz = current_field_types[part_clean]
                current_field_types = getattr(next_clazz, '__annotations__', {})
            final_key = parts[-1].replace('-', '_')
            if final_key not in current_field_types:
                raise KeyError(f'unexpected field "{final_key}" in path "{key}"')
            converted_value = parse_typed_object(value, current_field_types[final_key])
            setattr(current_obj, final_key, converted_value)
        else:
            key_clean = key.replace('-', '_')
            if key_clean not in field_types:
                raise KeyError(f'unexpected field "{key_clean}" provided for type {clazz.__name__}')
            converted_value = parse_typed_object(value, field_types[key_clean])
            setattr(obj, key_clean, converted_value)
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
    
    elif isinstance(clazz, type) and hasattr(clazz, '__annotations__') and clazz.__annotations__:
        assert isinstance(obj, dict), f'expected dict type to parse into {clazz.__name__}, got {type(obj)}'
        instance = clazz()
        field_types = clazz.__annotations__
        for key, value in obj.items():
            if key not in field_types:
                raise KeyError(f'unexpected field "{key}" provided to type {clazz.__name__}')
            setattr(instance, key, parse_typed_object(value, field_types[key]))
        return instance
    
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
