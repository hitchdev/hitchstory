from slugify import slugify


class HitchStoryException(Exception):
    pass


class StepNotFound(HitchStoryException):
    """
    Step in story has no corresponding method in engine.
    """
    pass


class StoryNotFound(HitchStoryException):
    """
    Story not found.
    """
    def __init__(self, name):
        super(HitchStoryException, self).__init__((
            "Story '{0}' not found.".format(name)
        ))


class StepException(HitchStoryException):
    """
    Exception relating to a particular step.
    """
    pass


class StepNotCallable(StepException):
    """
    The step you tried to call is not a python method.
    """
    pass


class StepContainsInvalidValidator(StepException):
    """
    Step contains a validator for which there is no corresponding argument.
    """
    pass


class StepArgumentWithoutValidatorContainsComplexData(StepException):
    """
    Step arguments that contain hierarchical data like so:

    - step name:
        complex argument:
          x: 1
          y: 2
        complex argument:
          - list item
          - list item

    need validators.
    """
    pass


class WrongEngineType(HitchStoryException):
    """
    Engine should inherit from hitchstory.BaseEngine.
    """
    pass


class MoreThanOneStory(HitchStoryException):
    """
    More than one story was found matching query.
    """
    def __init__(self, stories):
        super(HitchStoryException, self).__init__(
            "More than one matching story:\n{0}\n".format(stories)
        )


class NoStories(HitchStoryException):
    """
    User tried to use .one() but no stories were found.
    """
    pass


class DuplicateStoryNames(HitchStoryException):
    """
    Two or more stories in a collection have identical or too-similar names.
    """
    def __init__(self, story1, story2):
        super(HitchStoryException, self).__init__((
            "Story '{0}' in '{1}' and '{2}' in '{3}' are identical "
            "when slugified ('{4}' and '{5}')."
        ).format(
            story1.name,
            story1.filename,
            story2.name,
            story2.filename,
            slugify(story1.name),
            slugify(story2.name)
        ))


class InvalidStoryPaths(HitchStoryException):
    """
    storypaths iterator fed to StoryCollection is invalid.
    """
    pass
