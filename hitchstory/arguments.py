from hitchstory import utils, exceptions


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
            self.argument = self.parameterize(yaml_args)

    def parameterize(self, value):
        for name, parameter in self._params.items():
            value = utils.replace_parameter(value, str(name), str(parameter))
        return value

    def validate(self, validators):
        """
        Validate step using validators specified in decorators.
        """
        if not self.is_none and not self.single_argument:
            _kwargs = {}
            for key, value in self.original_args.items():
                if key in validators.keys():
                    _kwargs[key] = validators[key](value.value)
                else:
                    if not value.is_scalar():
                        raise exceptions.StepArgumentWithoutValidatorContainsComplexData
                    else:
                        _kwargs[key] = str(value)
            self.kwargs = self.parameterize(self.original_args)

    def pythonized_kwargs(self):
        pythonized_dict = {}
        for key, value in self.kwargs.items():
            pythonized_dict[utils.to_underscore_style(str(key))] = value.value
        return pythonized_dict
