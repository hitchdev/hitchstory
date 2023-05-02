from hitchstory.exceptions import Failure
from difflib import ndiff
import json


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


def json_match(expected, actual):
    """
    Check expected JSON string matches actual, raise Failure if they do not.
    """
    expected_parsed_json = json.loads(expected)
    actual_parsed_json = json.loads(actual)

    expected_cleaned_json = json.dumps(expected_parsed_json, sort_keys=True, indent=4)
    actual_cleaned_json = json.dumps(actual_parsed_json, sort_keys=True, indent=4)

    if expected_parsed_json != actual_parsed_json:
        raise Failure(
            "ACTUAL:\n{0}\n\nEXPECTED:\n{1}\n\nDIFF:\n{2}".format(
                actual_cleaned_json,
                expected_cleaned_json,
                "".join(
                    ndiff(
                        expected_cleaned_json.splitlines(1),
                        actual_cleaned_json.splitlines(1),
                    )
                ),
            )
        )
