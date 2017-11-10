from hitchstory.step_method import StepMethod
from hitchstory.arguments import Arguments
from hitchstory import exceptions
from hitchstory import utils


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
