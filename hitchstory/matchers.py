from hitchstory.exceptions import Failure
from difflib import ndiff


def strings_match(expected, actual):
    """
    Check expected string matches actual, raise Failure if they do not.
    """
    if expected != actual:
        raise Failure(
            "ACTUAL:\n{0}\n\nEXPECTED:\n{1}\n\nDIFF:\n{2}".format(
                actual,
                expected,
                "".join(ndiff(expected.splitlines(1), actual.splitlines(1))),
            )
        )
