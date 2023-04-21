from hitchstory import (
    StoryCollection,
    BaseEngine,
    exceptions,
    validate,
    no_stacktrace_for,
)
from hitchstory import GivenDefinition, GivenProperty, InfoDefinition, InfoProperty
from templex import Templex
from strictyaml import Optional, Str, Map, Int, Bool, Enum, load, MapPattern
from path import Path
from shlex import split
from templex import Templex
from commandlib import Command
from icommandlib import ICommand
from hitchrunpy import ExamplePythonCode, HitchRunPyException
import requests
import time


class Engine(BaseEngine):
    """Python engine for running tests."""

    def __init__(self, paths, rewrite=False):
        self._path = paths
        self._rewrite = rewrite

    def set_up(self):
        self.python = Command("/gen/devenv/bin/python")

    @no_stacktrace_for(AssertionError)
    @no_stacktrace_for(HitchRunPyException)
    @validate(
        code=Str(),
        will_output=Str(),
        raises=Map({Optional("type"): Str(), Optional("message"): Str()}),
    )
    def run(self, code, will_output=None, raises=None):
        self.example_py_code = (
            ExamplePythonCode(self.python, self._path.gen)
            .with_terminal_size(160, 160)
            .include_files(*self._path.project.joinpath("app").glob("*.py"))
        )
        to_run = self.example_py_code.with_code(code)

        result = (
            to_run.expect_exceptions().run() if raises is not None else to_run.run()
        )

        actual_output = result.output

        if will_output is not None:
            try:
                Templex(will_output).assert_match(actual_output)
            except AssertionError:
                if self._rewrite:
                    self.current_step.update(will_output=actual_output)
                else:
                    raise

        if raises is not None:
            exception_type = raises.get("type")
            message = raises.get("message")

            try:
                result.exception_was_raised(exception_type)
                exception_message = result.exception.message
                Templex(message).assert_match(exception_message)
            except AssertionError:
                if self._rewrite:
                    new_raises = raises.copy()
                    new_raises["message"] = exception_message
                    self.current_step.update(raises=new_raises)
                else:
                    raise

    def tear_down(self):
        pass

    def on_failure(self, result):
        pass

    def on_success(self):
        if self._rewrite:
            self.new_story.save()
