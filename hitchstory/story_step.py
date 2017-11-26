from hitchstory.step_method import StepMethod
from hitchstory.arguments import Arguments
from hitchstory import exceptions
from hitchstory import utils


class StoryStep(object):
    def __init__(self, story, yaml_step, index, child_index, params):
        self._yaml = yaml_step
        self._story = story
        self._index = index
        self._slug = None
        self._child_index = child_index
        if yaml_step.is_scalar():
            self.name = yaml_step.data
            self.arguments = Arguments(None, params)
        elif yaml_step.is_mapping():
            self.name = yaml_step.keys()[0].data
            self.arguments = Arguments(list(yaml_step.values())[0], params)
            StepMethod(self.step_method).revalidate(self.arguments)

    def underscore_case_name(self):
        return utils.to_underscore_style(self.name)

    def update(self, **kwargs):
        self._story.update(self, kwargs)

    @property
    def slug(self):
        return self.underscore_case_name()

    @property
    def index(self):
        return self._index

    @property
    def child_index(self):
        return self._child_index

    @property
    def yaml(self):
        return self._yaml

    def documentation(self, template=None):
        return utils.render_template(
            self._story._collection._templates,
            template if template is not None else self.slug,
            {"step": self, }
        )

    @property
    def _data(self):
        if self.arguments.single_argument:
            return {
                StepMethod(self.step_method).single_argument_name: self.arguments.data
            }
        return self.arguments.data

    def __getitem__(self, name):
        return self._data[name]

    def __contains__(self, name):
        return name in self._data

    @property
    def step_method(self):
        engine = self._story.engine
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

    def method(self):
        return StepMethod(self.step_method).method(self.arguments)

    def __repr__(self):
        return u"<StoryStep('{0}')>".format(self.slug)
