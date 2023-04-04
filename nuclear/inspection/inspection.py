from dataclasses import dataclass
import inspect as std_inspect
from typing import Any, List, Optional, Type, Iterable


@dataclass
class InspectConfig:
    attrs: bool
    dunder: bool
    full: bool


@dataclass
class InspectAttribute:
    name: str
    value: Any
    type: Type
    callable: bool
    dunder: bool
    private: bool
    signature: Optional[str]
    doc: Optional[str]


def inspect(
    obj: Any,
    *,
    attrs: bool = True,
    dunder: bool = False,
    full: bool = False,
):
    """
    Inspect object type and value and print its variables and methods
    :param obj: object to inspect
    :param attrs: whether to print attributes (variables and methods)
    :param dunder: whether to print dunder attributes
    :param full: whether to print non-abbreviated docs and values
    """
    print(inspect_format(obj, attrs=attrs, dunder=dunder, full=full))


ins = inspect  # alias


def inss(obj: Any, **kwargs):
    """Inspect short"""
    inspect(obj, attrs=False, **kwargs)


def insa(obj: Any, **kwargs):
    """Inspect all"""
    inspect(obj, attrs=True, dunder=True, **kwargs)


def inspect_format(
    obj: Any,
    *,
    attrs: bool = True,
    dunder: bool = False,
    full: bool = False,
) -> str:
    config = InspectConfig(attrs=attrs, dunder=dunder, full=full)

    str_value = _format_value(obj, config)
    str_type = _format_type(type(obj))
    output: List[str] = [
        f'{STYLE_BRIGHT_BLUE}value:{RESET} {str_value}',
        f'{STYLE_BRIGHT_BLUE}type:{RESET} {STYLE_YELLOW}{str_type}{RESET}',
    ]
 
    if callable(obj):
        signature = _get_callable_signature(obj.__name__, obj)
        output.append(f'{STYLE_BRIGHT_BLUE}signature:{RESET} {signature}')

    doc = _get_doc(obj, config)
    if doc:
        output.append(f'{STYLE_GRAY}# {doc}{RESET}')

    if config.attrs:
        attributes = sorted(_iter_attributes(obj, config), key=lambda attr: attr.name)
        output.extend(_format_attrs_section(attributes, config))

    return '\n'.join(line for line in output if line is not None)


def _iter_attributes(obj: Any, config: InspectConfig) -> Iterable[InspectAttribute]:
    keys = dir(obj)
    for key in keys:
        value = getattr(obj, key)
        callable_ = callable(value)
        dunder = key.startswith('__') and key.endswith('__')
        private = key.startswith('_') and not dunder
        signature = _get_callable_signature(key, value) if callable_ else None
        doc = _get_doc(value, config) if callable_ else None
        yield InspectAttribute(
            name=key,
            value=value,
            type=type(value),
            callable=callable_,
            dunder=dunder,
            private=private,
            signature=signature,
            doc=doc,
        )


def _get_callable_signature(name: str, obj: Any) -> Optional[str]:
    try:
        _signature = str(std_inspect.signature(obj))
    except (ValueError, TypeError):
        _signature = "(…)"
    
    if std_inspect.isclass(obj):
        prefix = "class"
    elif std_inspect.iscoroutinefunction(obj):
        prefix = "async def"
    else:
        prefix = "def"

    return f'{STYLE_BLUE}{prefix} {STYLE_BRIGHT_GREEN}{name}{STYLE_GREEN}{_signature}{RESET}'


def _get_doc(obj: Any, config: InspectConfig) -> Optional[str]:
    doc = std_inspect.getdoc(obj)
    if doc is None:
        return None
    return _shorten_string(doc.strip(), config)


def _format_attr_variable(attr: InspectAttribute, config: InspectConfig) -> str:
    value_str = _format_value(attr.value, config)
    type_str = _format_type(attr.type)
    return f'  {STYLE_BRIGHT_YELLOW}{attr.name}{STYLE_YELLOW}: {type_str} = {value_str}'


def _format_attr_method(attr: InspectAttribute) -> str:
    if not attr.signature:
        return f'  {attr.name}(…)'
    if attr.doc:
        return f'  {attr.signature}: {STYLE_GRAY}# {attr.doc}{RESET}'
    else:
        return f'  {attr.signature}'


def _format_value(value: Any, config: InspectConfig) -> str:
    if isinstance(value, str):
        return f"{STYLE_GREEN}'{_shorten_string(value, config)}'{RESET}"
    if value is None:
        return f'{STYLE_MAGENTA}None{RESET}'
    if value is True:
        return f'{STYLE_GREEN}True{RESET}'
    if value is False:
        return f'{STYLE_RED}False{RESET}'
    if isinstance(value, (int, float)):
        return f'{STYLE_RED}{value}{RESET}'
    return _shorten_string(str(value), config)


def _format_type(type_: Type) -> str:
    module = type_.__module__
    if module is None or module == str.__class__.__module__:  # built-in type
        return f'{STYLE_YELLOW}{type_.__name__}{RESET}'
    return f'{STYLE_YELLOW}{module}.{type_.__name__}{RESET}'


def _shorten_string(text: str, config: InspectConfig) -> str:
    if config.full:
        return text
    
    first_line, _, rest = text.partition('\n')
    if rest:
        first_line = first_line + '…'
    if len(first_line) > 100:
        first_line = first_line[:100] + '…'
    return first_line


def _format_attrs_section(attributes: List[InspectAttribute], config: InspectConfig) -> Iterable[str]:
    public_attrs = [attr for attr in attributes if not attr.private and not attr.dunder]
    private_attrs = [attr for attr in attributes if attr.private]
    dunder_attrs = [attr for attr in attributes if attr.dunder]

    public_vars = [attr for attr in public_attrs if not attr.callable]
    private_vars = [attr for attr in private_attrs if not attr.callable]
    dunder_vars = [attr for attr in dunder_attrs if not attr.callable]
    public_methods = [attr for attr in public_attrs if attr.callable]
    private_methods = [attr for attr in private_attrs if attr.callable]
    dunder_methods = [attr for attr in dunder_attrs if attr.callable]

    if public_vars or public_methods:
        yield ""
        yield f"{STYLE_BRIGHT}Public attributes:{RESET}"
        for attr in public_vars:
            yield _format_attr_variable(attr, config)
        if public_vars and public_methods:
            yield ""
        for attr in public_methods:
            yield _format_attr_method(attr)
    
    if private_vars or private_methods:
        yield ""
        yield f"{STYLE_BRIGHT}Private attributes:{RESET}"
        for attr in private_vars:
            yield _format_attr_variable(attr, config)
        if private_vars and private_methods:
            yield ""
        for attr in private_methods:
            yield _format_attr_method(attr)

    if config.dunder and dunder_attrs:
        yield ""
        yield f"{STYLE_BRIGHT}Dunder attributes:{RESET}"
        for attr in dunder_vars:
            yield _format_attr_variable(attr, config)
        if dunder_vars and dunder_methods:
            yield ""
        for attr in dunder_methods:
            yield _format_attr_method(attr)


RESET ='\033[0m'
STYLE_BRIGHT = '\033[1m'
STYLE_DIM = '\033[2m'

STYLE_RED = '\033[0;31m'
STYLE_BRIGHT_RED = '\033[1;31m'
STYLE_GREEN = '\033[0;32m'
STYLE_BRIGHT_GREEN = '\033[1;32m'
STYLE_YELLOW = '\033[0;33m'
STYLE_BRIGHT_YELLOW = '\033[1;33m'
STYLE_BLUE = '\033[0;34m'
STYLE_BRIGHT_BLUE = '\033[1;34m'
STYLE_MAGENTA = '\033[0;35m'
STYLE_CYAN = '\033[0;36m'
STYLE_WHITE = '\033[0;37m'
STYLE_GRAY = '\033[2;37m'
