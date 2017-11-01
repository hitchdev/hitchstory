"""
User-exposed engine related code.
"""
from hitchstory import exceptions
from strictyaml import MapPattern, Str, Any, Map, Validator, Optional
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


def expected_exception(exception_type):
    """
    Tag a method as expecting an exception of exception type.
    """
    def decorator(step_function):
        if not hasattr(step_function, '_expected_exceptions'):
            step_function._expected_exceptions = [exception_type, ]
        else:
            step_function._expected_exceptions.append(exception_type)
        return step_function
    return decorator


class StorySchema(object):
    """
    Represents user-defineable parts of the hitchstory schema:

    * preconditions - properties which set up the story.
    * parameters - variables which you can feed into a story.
    * about - descriptive properties - e.g. feature names, issue ticket numbers
    """
    def __init__(self, given=None, params=None, about=None):
        if given is None:
            self._preconditions = MapPattern(Str(), utils.YAML_Param | Any())
        else:
            _preconditions = {}
            for name, validator in given.items():
                assert isinstance(validator, Validator),\
                    "precondition schema must be strictyaml Validators"
                _preconditions[name] = utils.YAML_Param | validator
            self._preconditions = Map(_preconditions)

        if about is not None:
            assert isinstance(about, dict), "about must be a dict of named validators"
            for key, validator in about.items():
                assert isinstance(key, str) or isinstance(key, Optional), \
                    "name must be a string or strictyaml Optional."
                assert isinstance(validator, Validator), "validator must be strictyaml Validator"

        self._about = about

    @property
    def preconditions(self):
        return self._preconditions

    @property
    def about(self):
        return self._about


class NewStory(object):
    def __init__(self, engine):
        self._engine = engine

    def save(self):
        """
        Write out the updated story to file.
        """
        story_file = self._engine.story.story_file
        story_file.path.write_text(
            story_file._updated_yaml.as_yaml()
        )


class BaseEngine(object):
    schema = StorySchema()

    @property
    def new_story(self):
        return NewStory(self)

    @property
    def given(self):
        return self._preconditions

    def set_up(self):
        pass

    def on_abort(self, signal_num, stack_frame):
        pass

    def on_failure(self, report):
        pass

    def on_success(self):
        pass

    def tear_down(self):
        pass
