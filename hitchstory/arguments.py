from hitchstory import utils
from strictyaml import YAML, Any


class Arguments(object):
    """A null-argument, single argument or group of arguments of a hitchstory step."""

    def __init__(self, yaml_args, params):
        """Create arguments from dict (from yaml)."""
        self._params = params

        if yaml_args is None:
            self.is_none = True
            self.single_argument = False
        elif yaml_args.is_mapping():
            self.is_none = False
            self.single_argument = False
            self.original_args = yaml_args
        else:
            self.is_none = False
            self.single_argument = True
            self.argument = yaml_args

    def parameterize(self, value):
        """
        Take parameters in the story "My name is ((( name )))" and replace them
        with specified params, e.g. "My name is Tony".
        """
        for name, parameter in self._params.items():
            original_value = value.data if isinstance(value, YAML) else value
            value = utils.replace_parameter(original_value, str(name), str(parameter))
        return value

    def validate(self, validators):
        """
        Validate step using StrictYAML validators specified in @validate decorators.
        """
        if not self.is_none and not self.single_argument:
            _kwargs = {}
            for key, value in self.original_args.items():
                if str(key) in validators.keys():
                    _kwargs[key] = validators[key](value._chunk).data
                else:
                    _kwargs[key] = Any()(value._chunk).data

            self.kwargs = self.parameterize(_kwargs)
        if self.single_argument:
            if len(validators) == 0:
                self.argument = Any()(self.argument._chunk)
            else:
                self.argument = list(validators.values())[0](self.argument._chunk)
            self.argument = self.parameterize(self.argument)

    def pythonized_kwargs(self):
        """
        Convert keyword arguments from readable English (e.g. Do a thing)
        into an underscore style method name (do_a_thing).
        """
        pythonized_dict = {}
        for key, value in self.kwargs.items():
            pythonized_dict[utils.to_underscore_style(str(key))] = value.data \
                if isinstance(value, YAML) else value
        return pythonized_dict
