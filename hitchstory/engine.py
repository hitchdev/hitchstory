"""
User-exposed engine related code.
"""
from hitchstory import exceptions
from strictyaml import Any, Map, Optional
from hitchstory import utils


def validate(**kwargs):
    """
    Decorator for validating arguments in a HitchStory step.
    """

    def decorator(step_function):
        for arg in kwargs:
            if arg not in step_function.__code__.co_varnames:
                raise exceptions.StepContainsInvalidValidator(
                    "Step {} does not contain argument '{}' listed as a validator.".format(
                        step_function.__repr__(), arg
                    )
                )
        step_function._validators = kwargs
        return step_function

    return decorator


def no_stacktrace_for(exception_type):
    """
    Suppress stack trace for exceptions of exception_type on the
    method.
    """

    def decorator(step_function):
        if not hasattr(step_function, "_expected_exceptions"):
            step_function._expected_exceptions = [exception_type]
        else:
            step_function._expected_exceptions.append(exception_type)
        return step_function

    return decorator


def about(template):
    """
    Attach a template to a step which can be used to generate
    documentation about the step.
    """

    def decorator(step_function):
        step_function._about_template = template
        return step_function

    return decorator


class GivenProperty(object):
    def __init__(self, schema=None, document=None):
        self.schema = Any() if schema is None else schema
        self.document = document


class GivenDefinition(object):
    def __init__(self, **given_properties):
        self.given_properties = given_properties
        mapping = {}
        for name, given_property in given_properties.items():
            assert isinstance(
                given_property, GivenProperty
            ), "{0} must be GivenProperty.".format(name)
            mapping[Optional(name)] = utils.YAML_Param | given_property.schema
        self.preconditions = Map(mapping, key_validator=utils.UnderscoredSlug())

    @property
    def document_templates(self):
        return {name: prop.document for name, prop in self.given_properties.items()}

    def keys(self):
        return self.given_properties.keys()


class InfoProperty(object):
    def __init__(self, schema=None):
        self.schema = Any() if schema is None else schema


class InfoDefinition(object):
    def __init__(self, **info_properties):
        self._properties = {}
        for name, info_property in info_properties.items():
            assert isinstance(
                info_property, InfoProperty
            ), "{0} must be InfoProperty.".format(name)
            assert name not in [
                "based_on",
                "steps",
                "about",
                "with",
                "given",
                "variations",
                "examples",
            ], "{0} is not a valid name for an InfoProperty."
            self._properties[name] = info_property.schema

    def items(self):
        return self._properties.items()

    def keys(self):
        return self._properties.keys()


class NewStory(object):
    def __init__(self, engine):
        self._engine = engine

    def save(self):
        """
        Write out the updated story to file.
        """
        self._engine.story.story_file.rewrite()


class BaseEngine(object):
    given_definition = GivenDefinition()
    info_definition = InfoDefinition()

    @property
    def new_story(self):
        return NewStory(self)

    @property
    def given(self):
        return self._given

    def set_up(self):
        pass

    def on_abort(self, signal_num, stack_frame):
        self._aborted = True

    def on_failure(self, report):
        pass

    def on_success(self):
        pass

    def tear_down(self):
        pass
