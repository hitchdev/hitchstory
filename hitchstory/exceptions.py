class HitchStoryException(Exception):
    pass


class StepNotFound(HitchStoryException):
    pass


class StepException(HitchStoryException)
    pass


class StepNotCallable(StepException):
    pass


class StepNotDecorated(StepException):
    pass


class StepContainsInvalidValidator(StepException):
    pass


class StepArgumentWithoutValidatorContainsComplexData(StepException):
    pass