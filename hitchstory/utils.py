from strictyaml import Regex
from re import compile


PARAM_REGEX = r"^\(\((.*?)\)\)$"


YAML_Param = Regex(PARAM_REGEX)


def is_parameter(text):
    """
    Is the chunk of YAML data passed to us a parameter?

    i.e. like so (( parametername ))
    """
    return isinstance(text, str) and compile(PARAM_REGEX).match(text) is not None


def parameter_name(text):
    """
    Return parameter name from parameter text.

    e.g. (( param_name )) -> "param_name"
    """
    return compile(PARAM_REGEX).match(text).group(1).strip()


def to_underscore_style(text):
    """Changes "Something like this" to "something_like_this"."""
    text = text.lower().replace(" ", "_").replace("-", "_")
    return ''.join(x for x in text if x.isalpha() or x.isdigit() or x == "_")
