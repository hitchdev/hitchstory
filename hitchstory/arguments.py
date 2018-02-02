from collections import OrderedDict
from hitchstory import utils
from strictyaml import Map
from copy import copy


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
            self.yaml = yaml_args
        elif yaml_args.is_scalar():
            self.is_none = False
            self.single_argument = True
            self.yaml = yaml_args

    def parameterize(self, value):
        """
        Replace parameters with specified variables.
        """
        if isinstance(value, OrderedDict):
            parameterized_value = copy(value)

            for val_name, val_value in value.items():
                for param_name, param_value in self._params.items():
                    if utils.is_parameter(val_value):
                        if param_name == utils.parameter_name(val_value):
                            parameterized_value[val_name] = param_value

            return parameterized_value
        else:
            for name, parameter in self._params.items():
                if utils.is_parameter(value):
                    if name == utils.parameter_name(value):
                        return parameter
            return value

    def _revalidate(self, validator):
        self.yaml.revalidate(validator)

    def validate_args(self, validator):
        """
        Validate step using StrictYAML validators specified in @validate decorators.
        """
        self._revalidate(Map(validator, key_validator=utils.UnderscoredSlug()))
        self.data = {}

        for key, value in self.yaml.items():
            self.data[key.data] = self.parameterize(value.data)

    def validate_single_argument(self, validator):
        self.yaml.revalidate(validator)
        self.data = self.parameterize(self.yaml.data)

    def validate_kwargs(self, validator):
        self.yaml.revalidate(validator)
        self.data = self.parameterize(self.yaml.data)
