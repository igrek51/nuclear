import dataclasses
from datetime import date, datetime
import json
from pathlib import Path, PosixPath
from typing import Dict, List, Type, TypeVar

from pydantic import BaseModel
import yaml

T = TypeVar("T", bound=BaseModel)


def parse_dict_datamodel(
    obj_dict: Dict,
    clazz: Type[T], 
) -> T:
    """
    Cast dict object to expected pydantic model
    :param obj_dict: dict object to be transformed to pydantic.BaseModel
    :param clazz: pydantic.BaseModel type
    """
    return clazz.model_validate(obj_dict)


def parse_dict_datamodels(
    obj_list: List[Dict],
    clazz: Type[T],
) -> List[T]:
    """Cast list of dict objects to expected data model types (pydantic.BaseModel)"""
    return [parse_dict_datamodel(obj_dict, clazz) for obj_dict in obj_list]


def parse_yaml_datamodel(
    yaml_obj: str,
    clazz: Type[T],
) -> T:
    """
    Parse YAML and convert it to expected data model
    :param yaml_obj: YAML string
    :param clazz: pydantic.BaseModel type
    """
    data = yaml.load(yaml_obj, Loader=yaml.FullLoader)
    if data is None:
        data = {}
    return clazz.model_validate(data)


def parse_yaml_file_datamodel(
    path: Path,
    clazz: Type[T],
) -> T:
    """
    Parse YAML file and convert it to expected data model
    :param path: Path to a YAML file
    :param clazz: pydantic.BaseModel type
    """
    assert path.is_file(), f"File doesn't exist: {path}"
    data = path.read_text()
    return parse_yaml_datamodel(data, clazz)


def datamodel_to_yaml_str(dt: BaseModel) -> str:
    data_dict = datamodel_to_dict(dt)
    return yaml.dump(data_dict)


def to_json(obj) -> str:
    obj = to_json_serializable(obj)
    obj = remove_none(obj)
    return json.dumps(obj)


def to_yaml(obj) -> str:
    obj = to_json_serializable(obj)
    obj = remove_none(obj)
    return yaml.dump(obj, sort_keys=False)


def datamodel_to_dict(dt: BaseModel) -> Dict:
    data_dict = dt.model_dump()
    data_dict = remove_none(data_dict)
    data_dict = to_json_serializable(data_dict)
    return data_dict


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
    elif isinstance(obj, BaseModel):
        return obj.model_dump()
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
