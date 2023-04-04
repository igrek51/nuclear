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

    output: List[str] = [
        f'str: {str(obj)}',
        f'type: {type(obj)}',
    ]
    doc = _get_doc(obj, config)
    if doc:
        output.append(f'doc: {doc}')

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
        _signature = ""
    
    if std_inspect.isclass(obj):
        prefix = "class"
    elif std_inspect.iscoroutinefunction(obj):
        prefix = "async def"
    else:
        prefix = "def"

    return f'{prefix} {name}{_signature}'


def _get_doc(obj: Any, config: InspectConfig) -> Optional[str]:
    doc = std_inspect.getdoc(obj)
    if doc is None:
        return None
    return _shorten_string(doc.strip(), config)


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
        yield "Public attributes:"
        for attr in public_vars:
            yield _format_attr_variable(attr, config)
        if public_vars and public_methods:
            yield ""
        for attr in public_methods:
            yield _format_attr_method(attr)
    
    if private_vars or private_methods:
        yield ""
        yield "Private attributes:"
        for attr in private_vars:
            yield _format_attr_variable(attr, config)
        if private_vars and private_methods:
            yield ""
        for attr in private_methods:
            yield _format_attr_method(attr)

    if config.dunder and dunder_attrs:
        yield ""
        yield "Dunder attributes:"
        for attr in dunder_vars:
            yield _format_attr_variable(attr, config)
        if dunder_vars and dunder_methods:
            yield ""
        for attr in dunder_methods:
            yield _format_attr_method(attr)


def _format_attr_variable(attr: InspectAttribute, config: InspectConfig) -> str:
    value_str = _shorten_string(str(attr.value), config)
    if isinstance(attr.value, str):
        value_str = f"'{value_str}'"
    return f'  {attr.name}: {attr.type} = {value_str}'


def _format_attr_method(attr: InspectAttribute) -> str:
    if not attr.signature:
        return f'  {attr.name}(…)'
    if attr.doc:
        return f'  {attr.signature}: # {attr.doc}'
    else:
        return f'  {attr.signature}'


def _shorten_string(text: str, config: InspectConfig) -> str:
    if config.full:
        return text
    
    first_line, _, rest = text.partition('\n')
    if rest:
        first_line = first_line + '…'
    if len(first_line) > 100:
        first_line = first_line[:100] + '…'
    return first_line
