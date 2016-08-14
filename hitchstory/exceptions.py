class HitchStoryException(Exception):
    pass


class StepNotFound(HitchStoryException):
    pass


class StepNotCallable(HitchStoryException):
    pass


class StepNotDecorated(HitchStoryException):
    pass
