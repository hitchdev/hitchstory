from hitchstory.exceptions import Failure
from difflib import ndiff
import json


def _should_be_string(variable, type_of_string):
    if not isinstance(variable, str):
        raise Failure(
            (
                "strings_match(expected, actual) - {} should be a string. "
                "Instead it is of type {}.".format(
                    type_of_string,
                    str(type(variable)),
                )
            )
        )


def strings_match(expected, actual):
    """
    Check expected string matches actual, raise Failure if they do not.
    """
    _should_be_string(expected, "expected")
    _should_be_string(actual, "expected")

    if expected != actual:
        raise Failure(
            "ACTUAL:\n{0}\n\nEXPECTED:\n{1}\n\nDIFF:\n{2}".format(
                actual,
                expected,
                "".join(ndiff(expected.splitlines(1), actual.splitlines(1))),
            )
        )


def _json_should_be_string(variable, type_of_string):
    if not isinstance(variable, str):
        if isinstance(variable, dict):
            raise Failure(
                (
                    "json_match(expected, actual) - {} is a dict. It "
                    "should be a string of unparsed JSON.\n\n"
                    "You could try sending the original JSON string "
                    "or use json.dumps(the_dict)"
                ).format(type_of_string)
            )
        else:
            raise Failure(
                (
                    "json_match(expected, actual) - {} should be"
                    "a string, instead it is of type {}.".format(
                        type_of_string, str(type(variable))
                    )
                )
            )


def json_match(expected, actual):
    """
    Check expected JSON string matches actual, raise Failure if they do not.
    """
    _json_should_be_string(expected, "expected")
    _json_should_be_string(actual, "actual")

    try:
        expected_parsed_json = json.loads(expected)
    except json.decoder.JSONDecodeError:
        raise Failure(
            "json_match(expected, actual) - expected value is not valid JSON:\n\n{}".format(
                expected
            )
        )

    try:
        actual_parsed_json = json.loads(actual)
    except json.decoder.JSONDecodeError:
        raise Failure(
            "json_match(expected, actual) - actual value is not valid JSON:\n\n{}".format(
                actual
            )
        )

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
