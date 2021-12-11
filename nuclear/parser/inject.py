from inspect import getfullargspec, ismethod
from typing import Any, List
from typing import Dict, Mapping

from nuclear.args.container import ArgsContainer
from nuclear.builder.typedef import Action
from nuclear.sublog import log


def run_action(action: Action, internal_vars: Dict[str, Any]):
    if action:
        args, varargs, _, defaults, kwonlyargs, kwonlydefaults, annotations = getfullargspec(action)
        injectable_args = args + kwonlyargs
        if not injectable_args and varargs is None:
            action()
        else:
            if ismethod(action):
                injectable_args = injectable_args[1:]  # drop 'self'
            action_kwargs = inject_args(injectable_args, action, annotations, internal_vars)
            if varargs is None:
                action(**action_kwargs)
            else:
                action_args = inject_arg(varargs, action, annotations, internal_vars)
                action(*action_args, **action_kwargs)


def inject_args(args: List[str], action: Action, annotations: Mapping[str, Any], internal_vars: Dict[str, Any]
                ) -> Dict[str, Any]:
    return {arg: inject_arg(arg, action, annotations, internal_vars) for arg in args}


def inject_arg(arg: str, action: Action, annotations: Mapping[str, Any], internal_vars: Dict[str, Any]) -> Any:
    if arg in internal_vars:
        return internal_vars[arg]
    elif is_args_container_name(arg, annotations):
        return ArgsContainer(internal_vars)
    else:
        log.warn(f"can't inject argument '{arg}' to function '{action.__name__}': name not found")
        return None


def is_args_container_name(arg: str, annotations: Mapping[str, Any]):
    if arg == 'args':
        if arg in annotations:  # has type annotation
            return annotations[arg] == ArgsContainer
        return True
    return False
