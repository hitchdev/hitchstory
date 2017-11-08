from hitchstory.arguments import Arguments
from hitchstory import exceptions
from hitchstory import utils
from strictyaml import Any, Optional
import inspect


class StepMethod(object):
    def __init__(self, method):
        self._method = method
        if self.argspec.varargs is not None:
            raise Exception("Illegal method")
        if self._keywords and len(self._args) > 1:
            raise Exception("Illegal method")

    @property
    def argspec(self):
        return inspect.getargspec(self._method)

    @property
    def _defaults(self):
        return self.argspec.defaults if self.argspec.defaults is not None else []

    @property
    def _args(self):
        return self.argspec.args if self.argspec.args is not None else []

    @property
    def _specified_validators(self):
        return self._method._validators if hasattr(self._method, '_validators') else {}

    @property
    def _keywords(self):
        return self.argspec.keywords is not None

    def arg_validator(self, name):
        return utils.YAML_Param | self._specified_validators.get(name, Any())

    @property
    def optional_args(self):
        return self.argspec.args[len(self._defaults) - len(self._args):]

    @property
    def required_args(self):
        return self.argspec.args[:len(self._defaults) - len(self._args)][1:]

    @property
    def single_argument_allowed(self):
        return len(self.required_args) == 0 and len(self.optional_args) > 0 \
            or len(self.required_args) == 1

    @property
    def single_argument_name(self):
        return self.argspec.args[1]

    @property
    def mapping_validators(self):
        validators = {}
        for arg in self.optional_args:
            validators[Optional(arg)] = self.arg_validator(arg)
        for arg in self.required_args:
            validators[arg] = self.arg_validator(arg)
        return validators

    def run(self, arguments):
        if arguments.is_none:
            self._method()
        elif arguments.single_argument:
            if self.single_argument_allowed:
                arguments.validate_single_argument(self.arg_validator(self.single_argument_name))
                self._method(**{self.single_argument_name: arguments.data})
            else:
                raise Exception("More than one argument required")
        else:
            if self._keywords:
                arguments.validate_kwargs(self.arg_validator(self._keywords))
                self._method(**arguments.data)
            else:
                arguments.validate_args(self.mapping_validators)
                self._method(**arguments.data)


class StoryStep(object):
    def __init__(self, story, yaml_step, index, child_index, params):
        self._yaml = yaml_step
        self._story = story
        self._index = index
        self._child_index = child_index
        if isinstance(yaml_step.value, str):
            self.name = str(yaml_step)
            self.arguments = Arguments(None, params)
        elif isinstance(yaml_step.value, dict) and len(yaml_step.keys()) == 1:
            self.name = str(list(yaml_step.keys())[0])
            self.arguments = Arguments(list(yaml_step.values())[0], params)
        else:
            raise RuntimeError("Invalid YAML in step '{}'".format(yaml_step))

    def underscore_case_name(self):
        return utils.to_underscore_style(str(self.name))

    def update(self, **kwargs):
        self._story.update(self, kwargs)

    @property
    def index(self):
        return self._index

    @property
    def child_index(self):
        return self._child_index

    @property
    def yaml(self):
        return self._yaml

    @property
    def step_method(self):
        engine = self._story._engine
        if hasattr(engine, self.underscore_case_name()):
            attr = getattr(engine, self.underscore_case_name())
            if hasattr(attr, '__call__'):
                return attr
            else:
                raise exceptions.StepNotCallable((
                    "Step with name '{}' in {} is not a function "
                    "or a callable object, it is a {}".format(
                        self.underscore_case_name(),
                        engine.__repr__(),
                        type(attr)
                    )
                ))
        else:
            raise exceptions.StepNotFound("Step with name '{}' not found in {}.".format(
                self.underscore_case_name(),
                engine.__repr__()
            ))

    def expect_exception(self, engine, exception):
        if isinstance(exception, exceptions.Failure):
            return True

        try:
            step_method = self.step_method
        except exceptions.HitchStoryException:
            return False

        if hasattr(step_method, '_expected_exceptions'):
            return isinstance(exception, tuple(step_method._expected_exceptions))

        return False

    def run(self):
        StepMethod(self.step_method).run(self.arguments)
