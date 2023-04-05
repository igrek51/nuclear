from dataclasses import dataclass
import inspect as std_inspect
import os
import re
import sys
from typing import Any, Dict, List, Optional, Type, Iterable


@dataclass
class InspectConfig:
    attrs: bool
    dunder: bool
    docs: bool
    long: bool
    long_docs: bool
    code: bool


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
    docs: bool = True,
    long: bool = False,
    long_docs: bool = False,
    code: bool = False,
    all: bool = False,
):
    """
    Examine the object's information, such as its type, formatted value, variables, methods,
    documentation or source code.
    :param obj: object to inspect
    :param attrs: whether to print attributes (variables and methods)
    :param dunder: whether to print dunder attributes
    :param docs: whether to print documentation
    :param long: whether to print non-abbreviated values
    :param long_docs: whether to print non-abbreviated documentation
    :param code: whether to print source code of a function, method or class
    :param all: whether to include all information
    """
    print(inspect_format(
        obj, attrs=attrs or all, dunder=dunder or all, long=long or all, docs=docs or all,
        long_docs=long_docs or all, code=code or all))


def insp(obj: Any, **kwargs):
    """Examine object's attributes (variables and methods)"""
    inspect(obj, **kwargs)


def ins(obj: Any, **kwargs):
    """Examine object's elementary data"""
    inspect(obj, attrs=False, **kwargs)


def insl(obj: Any, **kwargs):
    """Examine object's attributes, long (non-abbreviated) values and docs"""
    inspect(obj, long=True, long_docs=True, **kwargs)


def insa(obj: Any, **kwargs):
    """Examine all object's information"""
    inspect(obj, all=True, **kwargs)


def inspect_format(
    obj: Any,
    *,
    attrs: bool = True,
    dunder: bool = False,
    docs: bool = True,
    long: bool = False,
    long_docs: bool = False,
    code: bool = False,
) -> str:
    config = InspectConfig(attrs=attrs, dunder=dunder, docs=docs, long=long, long_docs=long_docs, code=code)

    str_value = _format_value(obj)
    str_type = _format_type(type(obj))
    output: List[str] = [
        f'{STYLE_BRIGHT_BLUE}value:{RESET} {str_value}',
        f'{STYLE_BRIGHT_BLUE}type:{RESET} {STYLE_YELLOW}{str_type}{RESET}',
    ]
 
    if callable(obj):
        signature = _get_callable_signature(obj.__name__, obj)
        output.append(f'{STYLE_BRIGHT_BLUE}signature:{RESET} {signature}')

    doc = _get_doc(obj, long=True)
    if doc and config.docs:
        output.append(f'{STYLE_GRAY}"""\n{doc}\n"""{RESET}')

    if config.code and (std_inspect.isclass(obj) or callable(obj)):
        source = _get_source_code(obj)
        if source:
            output.append(f'{STYLE_BRIGHT_BLUE}source code:{RESET}\n{source}')

    if config.attrs:
        attributes = sorted(_iter_attributes(obj, config), key=lambda attr: attr.name)
        output.extend(_render_attrs_section(attributes, config))

    if sys.stdout.isatty():  # horizontal bar
        terminal_width = os.get_terminal_size().columns
        output.insert(0, STYLE_BLUE + '─' * terminal_width + RESET)
        output.append(STYLE_BLUE + '─' * terminal_width + RESET)

    text = '\n'.join(line for line in output if line is not None)
    if not sys.stdout.isatty():
        text = _strip_color(text)
    return text


def _iter_attributes(obj: Any, config: InspectConfig) -> Iterable[InspectAttribute]:
    keys = dir(obj)
    for key in keys:
        value = getattr(obj, key)
        callable_ = callable(value)
        dunder = key.startswith('__') and key.endswith('__')
        private = key.startswith('_') and not dunder
        signature = _get_callable_signature(key, value) if callable_ else None
        doc = _get_doc(value, long=config.long_docs) if callable_ else None
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


def _get_source_code(obj: Any) -> Optional[str]:
    try:
        return std_inspect.getsource(obj)
    except (OSError, TypeError, IndentationError):
        return None


def _get_doc(obj: Any, long: bool) -> Optional[str]:
    doc = std_inspect.getdoc(obj)
    if doc is None:
        return None
    doc = doc.strip()
    if long:
        return doc
    else:
        return _shorten_string(doc)


def _render_attr_variable(attr: InspectAttribute, config: InspectConfig) -> str:
    value_str = _format_short_value(attr.value, long=config.long)
    type_str = _format_type(attr.type)
    return f'  {STYLE_BRIGHT_YELLOW}{attr.name}{STYLE_YELLOW}: {type_str} = {value_str}'


def _render_attr_method(attr: InspectAttribute) -> str:
    if not attr.signature:
        return f'  {attr.name}(…)'
    if attr.doc:
        return f'  {attr.signature}: {STYLE_GRAY}# {attr.doc}{RESET}'
    else:
        return f'  {attr.signature}'


def _format_short_value(value: Any, long: bool) -> str:
    value_str = _format_value(value)
    if long:
        return value_str
    return _shorten_string(value_str)


def _format_value(value: Any, indent: int = 0) -> str:
    if isinstance(value, str):
        return f"{STYLE_GREEN}'{value}'{RESET}"
    if value is None:
        return f'{STYLE_MAGENTA}None{RESET}'
    if value is True:
        return f'{STYLE_GREEN}True{RESET}'
    if value is False:
        return f'{STYLE_RED}False{RESET}'
    if isinstance(value, (int, float)):
        return f'{STYLE_RED}{value}{RESET}'
    if isinstance(value, dict):
        return _format_dict_value(value, indent=indent+1)
    if isinstance(value, list):
        return _format_list_value(value, indent=indent+1)
    return str(value)


def _format_dict_value(dic: Dict, indent: int) -> str:
    lines: List[str] = []
    indentation = '    ' * indent
    for key, value in dic.items():
        key_str = _format_value(key, indent)
        value_str = _format_value(value, indent)
        lines.append(f'{indentation}{key_str}: {value_str},')
    if lines:
        small_indent = "    " * (indent-1)
        middle_lines = '\n'.join(lines)
        return f'{STYLE_YELLOW}{{{RESET}\n{middle_lines}\n{small_indent}{STYLE_YELLOW}}}{RESET}'
    else:
        return f'{STYLE_YELLOW}{{}}{RESET}'


def _format_list_value(l: List, indent: int) -> str:
    lines: List[str] = []
    for value in l:
        value_str = _format_value(value, indent)
        lines.append('    ' * indent + f'{value_str},')
    if lines:
        small_indent = "    " * (indent-1)
        middle_lines = '\n'.join(lines)
        return f'{STYLE_YELLOW}[{RESET}\n{middle_lines}\n{small_indent}{STYLE_YELLOW}]{RESET}'
    else:
        return f'{STYLE_YELLOW}[]{RESET}'


def _format_type(type_: Type) -> str:
    module = type_.__module__
    if module is None or module == str.__class__.__module__:  # built-in type
        return f'{STYLE_YELLOW}{type_.__name__}{RESET}'
    return f'{STYLE_YELLOW}{module}.{type_.__name__}{RESET}'


def _shorten_string(text: str) -> str:
    first_line, _, rest = text.partition('\n')
    if rest:
        first_line = first_line + '…'
    if len(first_line) > 100:
        first_line = first_line[:100] + '…'
    return first_line + RESET


def _render_attrs_section(attributes: List[InspectAttribute], config: InspectConfig) -> Iterable[str]:
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
            yield _render_attr_variable(attr, config)
        if public_vars and public_methods:
            yield ""
        for attr in public_methods:
            yield _render_attr_method(attr)
    
    if private_vars or private_methods:
        yield ""
        yield f"{STYLE_BRIGHT}Private attributes:{RESET}"
        for attr in private_vars:
            yield _render_attr_variable(attr, config)
        if private_vars and private_methods:
            yield ""
        for attr in private_methods:
            yield _render_attr_method(attr)

    if config.dunder and dunder_attrs:
        yield ""
        yield f"{STYLE_BRIGHT}Dunder attributes:{RESET}"
        for attr in dunder_vars:
            yield _render_attr_variable(attr, config)
        if dunder_vars and dunder_methods:
            yield ""
        for attr in dunder_methods:
            yield _render_attr_method(attr)


def _strip_color(text: str) -> str:
    return re.sub(r'\x1b\[\d+(;\d+)?m', '', text)


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
