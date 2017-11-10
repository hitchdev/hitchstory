from slugify import slugify


class HitchStoryException(Exception):
    pass


class CannotMixKeywordArgs(HitchStoryException):
    """
    **kwargs and regular args cannot be mixed in story step methods.
    """
    pass


class CannotUseVarargs(HitchStoryException):
    """
    *args is not usable in step method.
    """
    pass


class StepMethodNeedsMoreThanOneArgument(HitchStoryException):
    """
    Method in story engine takes more than one argument.
    """
    pass


class StepNotFound(HitchStoryException):
    """
    Step in story has no corresponding method in engine.
    """
    pass


class FileNotFound(HitchStoryException):
    """
    Specified file not found.
    """
    def __init__(self, filename):
        super(HitchStoryException, self).__init__((
            "File '{0}' not found.".format(filename)
        ))


class StoryYAMLError(HitchStoryException):
    """
    YAML error found parsing a story file.
    """
    def __init__(self, filename, error):
        super(HitchStoryException, self).__init__((
            "YAML Error in file '{0}':\n{1}".format(filename, error)
        ))


class StoryNotFound(HitchStoryException):
    """
    Story not found.
    """
    def __init__(self, name):
        super(HitchStoryException, self).__init__((
            "Story '{0}' not found.".format(name)
        ))


class BasedOnStoryNotFound(HitchStoryException):
    """
    Story that other story inherits from is not found.
    """
    def __init__(self, inherited_story_name, inheriting_story_name, inheriting_story_filename):
        super(HitchStoryException, self).__init__((
            "Story '{0}' which '{1}' in '{2}' is based upon not found.".format(
                inherited_story_name,
                inheriting_story_name,
                inheriting_story_filename,
            )
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


class HitchStorySpecialMethodException(HitchStoryException):
    """
    Exception was raised in a special method:
    on_success, on_failure, tear_down
    """
    def __init__(self, stacktrace):
        super(HitchStorySpecialMethodException, self).__init__(
            "Stacktrace:\n{0}\n".format(stacktrace)
        )


class OnSuccessException(HitchStorySpecialMethodException):
    """
    Exception occurred in on_success method.
    """
    pass


class OnFailureException(HitchStorySpecialMethodException):
    """
    Exception occurred in on_failure method.
    """
    pass


class TearDownException(HitchStorySpecialMethodException):
    """
    Exception occurred in tear_down method.
    """
    pass


class Failure(Exception):
    """
    Test failed.
    """
    pass
