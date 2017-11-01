from hitchstory.arguments import Arguments
from hitchstory import exceptions
from hitchstory import utils
from strictyaml import YAML
import inspect


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

    def step_method(self, engine):
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
            step_method = self.step_method(engine)
        except exceptions.HitchStoryException:
            return False

        if hasattr(step_method, '_expected_exceptions'):
            return isinstance(exception, tuple(step_method._expected_exceptions))

        return False

    def run(self, engine):
        step_method = self.step_method(engine)

        validators = step_method._validators \
            if hasattr(step_method, '_validators') else {}
        self.arguments.validate(validators)

        if self.arguments.is_none:
            step_method()
        elif self.arguments.single_argument:
            if isinstance(self.arguments.argument, YAML):
                step_method(self.arguments.argument.value)
            else:
                step_method(self.arguments.argument)
        else:
            argspec = inspect.getargspec(step_method)

            if argspec.keywords is not None:
                kwargs = {
                    key.data: val for key, val in
                    self.arguments.kwargs.items()
                }
                step_method(**kwargs)
            else:
                step_method(**self.arguments.pythonized_kwargs())
