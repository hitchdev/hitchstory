from strictyaml import Regex, ScalarValidator
from re import compile
from path import Path
import prettystack
from jinja2.environment import Environment
from jinja2 import DictLoader
from slugify import slugify
import sys


SRC_DIR = Path(__file__).realpath().dirname()

TEMPLATE_DIR = SRC_DIR.joinpath("templates")


DEFAULT_STACK_TRACE = (
    prettystack.PrettyStackTemplate()
    .to_console()
    .cut_calling_code(SRC_DIR.joinpath("story.py"))
)


PARAM_REGEX = r"^\(\((.*?)\)\)$"


YAML_Param = Regex(PARAM_REGEX)


class UnderscoredSlug(ScalarValidator):
    def validate_scalar(self, chunk):
        return slugify(chunk.contents, separator="_")


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
    return "".join(x for x in text if x.isalpha() or x.isdigit() or x == "_")


def underscore_slugify(text):
    """Changes "Something like this" to "something_like_this"."""
    return slugify(text, separator="_")


def render_template(templates_dict, template_name, parameters):
    """
    Render a jinja2 template.
    """
    env = Environment()
    env.loader = DictLoader(templates_dict)
    return env.get_template(template_name).render(**parameters)


def current_stack_trace_data():
    """
    Build a list of tracebacks from the last stack trace
    including line numbers and filenames.

    All the data needed to build a pretty stacktrace.
    """
    tb_id = 0
    _, exception, tb = sys.exc_info()

    if exception is None:
        return None

    # Create list of tracebacks
    tracebacks = []
    while tb is not None:
        filename = tb.tb_frame.f_code.co_filename
        if filename == "<frozen importlib._bootstrap>":
            break

        tracebacks.append(
            {
                "tb_id": tb_id,
                "filename": tb.tb_frame.f_code.co_filename,
                "line": tb.tb_lineno,
                "function": tb.tb_frame.f_code.co_name,
            }
        )

        tb_id = tb_id + 1
        tb = tb.tb_next

    return {
        "tracebacks": tracebacks,
        "exception_string": str(exception),
        "docstring": exception.__doc__ if exception.__doc__ is not None else None,
        "exception_type": "{}.{}".format(
            type(exception).__module__, type(exception).__name__
        ),
    }
