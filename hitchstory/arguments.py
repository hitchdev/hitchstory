from hitchstory import utils
from ruamel.yaml.comments import CommentedMap


class Arguments(object):
    """A null-argument, single argument or group of arguments of a hitchstory step."""

    def __init__(self, yaml_args):
        """Create arguments from dict (from yaml)."""
        if yaml_args is None:
            self.is_none = True
            self.single_argument = False
        elif type(yaml_args) is CommentedMap:
            self.is_none = False
            self.single_argument = False
            self.kwargs = yaml_args
        else:
            self.is_none = False
            self.single_argument = True
            self.argument = yaml_args

    def validate(self, validators):
        if self.is_none:
            return
        elif self.single_argument:
            return
        else:
            _kwargs = {}
            for key, value in self.kwargs.items():
                if key in validators.keys():
                    print(value)
                    print(validators[key])
                    _kwargs[key] = validators[key](value)
            self.kwargs = _kwargs
            return

    def pythonized_kwargs(self):
        pythonized_dict = {}
        for key, value in self.kwargs.items():
            pythonized_dict[utils.to_underscore_style(key)] = value
        return pythonized_dict

    def to_dict(self):
        if self.is_none:
            return None
        elif self.single_argument:
            return self.argument
        else:
            return self.kwargs
