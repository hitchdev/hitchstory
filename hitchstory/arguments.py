from hitchstory import utils
from strictyaml import ScalarValidator, Map
from slugify import slugify


class UnderscoreCase(ScalarValidator):
    def validate_scalar(self, chunk):
        return slugify(chunk.contents, separator='_')


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
        for name, parameter in self._params.items():
            if utils.is_parameter(value):
                if name == utils.parameter_name(value):
                    return parameter
        return value

    def validate_args(self, validator):
        """
        Validate step using StrictYAML validators specified in @validate decorators.
        """
        self.yaml.revalidate(Map(validator, key_validator=UnderscoreCase()))
        self.data = {}

        for key, value in self.yaml.items():
            self.data[key.data] = self.parameterize(value.data)

    def validate_single_argument(self, validator):
        self.yaml.revalidate(validator)
        self.data = self.parameterize(self.yaml.data)

    def validate_kwargs(self, validator):
        self.yaml.revalidate(validator)
        self.data = self.parameterize(self.yaml.data)
