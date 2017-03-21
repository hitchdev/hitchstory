"""
User-exposed engine related code.
"""
from hitchstory import exceptions
from strictyaml import MapPattern, Any


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


class StorySchema(object):
    """
    Represents user-defineable parts of the hitchstory schema:

    * preconditions - properties which set up the story.
    * parameters - variables which you can feed into a story.
    * about - descriptive properties - e.g. feature names, issue ticket numbers
    """
    def __init__(self, preconditions=None, params=None, about=None):
        self._preconditions = MapPattern(Any(), Any()) if preconditions is None else preconditions
        self._params = MapPattern(Any(), Any()) if params is None else params
        self._about = about

    @property
    def preconditions(self):
        return self._preconditions

    @property
    def params(self):
        return self._params

    @property
    def about(self):
        return self._about


class BaseEngine(object):
    schema = StorySchema()

    @property
    def preconditions(self):
        return self._preconditions

    def set_up(self):
        pass

    def on_failure(self):
        pass

    def on_success(self):
        pass

    def tear_down(self):
        pass
