from typing import Union, Callable, Optional, List, Type, Any

from .rule import SubcommandRule, PrimaryOptionRule, ParameterRule, PositionalArgumentRule, ManyArgumentsRule, \
    DefaultActionRule, FlagRule


def subcommand(
        *keywords: str,
        run: Optional[Callable[..., None]] = None,
        help: str = None,
) -> SubcommandRule:
    """
    Create Subcommand rule specification.
    Subcommand is a keyword which narrows down the context and can execute an action.
    Subcommands may have multiple levels and may build a tree.
    It's similar to 'git' syntax: 'git remote rename ...'
    Subcommand can have more subrules which are activated only when corresponding subcommand is active.
    Subrules can be added using 'has' method.
    :param keywords: keyword arguments which any of them triggers a subcommand
    :param run: optional action to be invoked when subcommand is matched
    :param help: description of the subcommand displayed in help output
    :return: new subcommand rule specification
    """
    return SubcommandRule(help, set(keywords), run)


def flag(
        *keywords: str,
        help: str = None,
        multiple: bool = False,
) -> FlagRule:
    """
    Create flag rule specification.
    Flag is a boolean parameter which is toggled by single argument
    :param keywords: keyword arguments which any of them enables flag when it occurs.
    Flag keywords may be passed using direct format: '-f' or '--flag',
    as well as by name: 'f' or 'flag', which will be evaluated to '-f' or '--flag'.
    Single character flags will get single hyphen prefix (-f),
    longer flag names will get double hyphen prefix (--flag)
    :param help: description of the flag displayed in help output
    :param multiple: whether flag is allowed to occur many times.
    Then flag has int type and stores number of its occurrences
    :return: new flag rule specification
    """
    return FlagRule(set(keywords), help, multiple)


def parameter(
        *keywords: str,
        name: str = None,
        help: str = None,
        required: bool = False,
        default: Any = None,
        type: Union[Type, Callable[[str], Any]] = str,
        choices: Union[List[Any], Callable[..., List[Any]]] = None,
        multiple: bool = False,
) -> ParameterRule:
    """
    Create parameter rule specification.
    Parameter is a named value, which will be injected to triggered action by its name.
    Shell syntax for settings parameter value is following:
    '--parameter-name value' or '--parameter-name=value'
    The parameters may be later referenced by its name or keywords
    (in lowercase format without hyphen prefix and with underscores instead of dashes,
    e.g. '--paramater-name' will be injected as 'parameter_name')
    :param keywords: keyword arguments which are matched to parameter.
    Parameter keywords may be passed using direct format: '-p' or '--param',
    as well as by name: 'p' or 'param', which will be evaluated to '-p' or '--param'.
    Single character parameter will get single hyphen prefix (-p),
    longer parameter names will get double hyphen prefix (--param)
    :param name: explicit internal paramter name (can be used, when it's different from any keyword)
    :param help: description of the parameter displayed in help output
    :param required: whether parameter is required.
    If it's required but it's not given, the syntax error will be raised.
    :param default: default value for the parameter, if it's not given (and it's not required)
    :param type: type of parameter value (e.g. str, int, float)
    Reference to a parser function may be provided here as well.
    Then parameter value is evaluated by passing the string argument value to that function.
    :param choices: Explicit list of available choices for the parameter value
    or reference to a function which will be invoked to retrieve such possible values list.
    :param multiple: whether parameter is allowed to occur many times.
    Then parameter has list type and stores list of values
    :return: new parameter rule specification
    """
    return ParameterRule(set(keywords), name, required, default, type, choices, help, multiple)


def argument(
        name: str,
        help: str = None,
        required: bool = True,
        default: Any = None,
        type: Union[Type, Callable[[str], Any]] = str,
        choices: Union[List[Any], Callable[..., List[Any]]] = None,
) -> PositionalArgumentRule:
    """
    Create positional argument rule specification.
    Positional argument is an unnamed param
    which is recognized by its position in the command line arguments list.
    :param name: internal argument name, which will be used to reference argument value
    :param help: description of the argument displayed in help output
    :param required: whether positional argument is required.
    If it's required but it's not given, the syntax error will be raised.
    :param default: default value for the argument, if it's not given (and it's not required)
    :param type: explicit type of argument value (e.g. str, int, float)
    Reference to a parser function may be provided here as well.
    Then argument value is evaluated by passing the string argument value to that function.
    :param choices: Explicit list of available choices for the argument value
    or reference to a function which will be invoked to retrieve such possible values list.
    :return: new positional argument rule specification
    """
    return PositionalArgumentRule(name, required, default, type, choices, help)

# TODO parse types, autocomplete choices, many arguments rule with count set
def arguments(
        name: str,
        type: Union[Type, Callable[[str], Any]] = str,
        choices: Union[List[Any], Callable[..., List[Any]]] = None,
        count: Optional[int] = None,
        min_count: Optional[int] = None,
        max_count: Optional[int] = None,
        joined_with: Optional[str] = None,
        help: str = None,
) -> ManyArgumentsRule:
    """
    Create 'Multiple arguments' rule specification.
    It allows to retrieve specific number of CLI argumetns or all remaining arguments,
    which were not matched before.
    All matched arguments will be extracted to a list of arguments or a string (depending on joined_with parameter)
    :param name: internal variable name, which will be used to reference matched arguments list
    :param type: explicit type of arguments values (e.g. str, int, float)
    Reference to a parser function may be provided here as well.
    Then argument value is evaluated by passing the string argument value to that function.
    :param choices: Explicit list of available choices for the argument value
    or reference to a function which will be invoked to retrieve such possible values list.
    :param count: explicit number of arguments to retrieve.
    If undefined, there is no validation for arguments count.
    If you need particular number of arguments, you can use this count instead of setting min_count=max_count.
    :param min_count: minimum number of arguments.
    By default, there is no lower limit (it is 0).
    :param max_count: maximum number of arguments.
    If undefined, there is no upper limit for arguments count.
    :param joined_with: optional string joiner for arguments.
    If it's set, all matched arguments will be joined to string with that joiner.
    It it's not given, matched arguments will be passed as list of strings.
    This value (string or list) can be accessed by specified name, when it's being injected to a function.
    :param help: description of the arguments displayed in help output
    :return: new all remaining arguments rule specification
    """
    return ManyArgumentsRule(help, name, type, choices, count, min_count, max_count, joined_with)


def default_action(
        run: Callable[..., None] = None,
) -> DefaultActionRule:
    """
    Sets default action for CLI Builder or subcommand.
    Default action is a function which is invoked when no other, more specific rule is matched.
    Any parameters, flags and named arguments which are parameters of action function
    will be automatically injected based on parsed arguments.
    :param run: reference to a function wchich will be invoked
    :return: new default action specification
    """
    return DefaultActionRule(run)


def primary_option(
        *keywords: str,
        run: Callable[..., None] = None,
        help: str = None,
) -> PrimaryOptionRule:
    """
    Create Primary option rule specification.
    Primary option is a keyword which instantly triggers an action when it's detected,
    e.g. '--help', '--version'. It runs only specified action and stops further analyzing.
    :param keywords: keyword arguments, any of them triggers action from primary option
    :param run: action to be invoked when primary option is matched
    :param help: description of the primary option displayed in help output
    :return: new primary option rule specification
    """
    return PrimaryOptionRule(help, set(keywords), run)
