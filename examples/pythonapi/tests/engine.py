from hitchstory import StoryCollection, BaseEngine
from hitchstory import GivenDefinition, GivenProperty, InfoDefinition, InfoProperty
from hitchstory import Failure, strings_match, no_stacktrace_for
from hitchstory import exceptions, validate
from strictyaml import Optional, Str, Map, Int, Bool, Enum, load, MapPattern
from hitchrunpy import ExamplePythonCode, HitchRunPyException
from icommandlib import ICommand
from commandlib import Command
from pathlib import Path
from shlex import split
import requests
import time

PROJECT_DIR = Path(__file__).absolute().parents[0].parent

GEN_DIRECTORY = Path("/gen")


class Engine(BaseEngine):
    """Python engine for running tests."""

    def __init__(self, rewrite=False):
        self._rewrite = rewrite

    def set_up(self):
        self.python = Command(f"{GEN_DIRECTORY}/devenv/bin/python")

    @no_stacktrace_for(HitchRunPyException)
    @validate(
        code=Str(),
        will_output=Str(),
        raises=Map({Optional("type"): Str(), Optional("message"): Str()}),
    )
    def run(self, code, will_output=None, raises=None):
        self.example_py_code = (
            ExamplePythonCode(self.python, GEN_DIRECTORY)
            .with_terminal_size(160, 160)
            .include_files(*PROJECT_DIR.joinpath("app").glob("*.py"))
        )
        to_run = self.example_py_code.with_code(code)

        result = (
            to_run.expect_exceptions().run() if raises is not None else to_run.run()
        )

        actual_output = result.output

        if will_output is not None:
            try:
                strings_match(will_output, actual_output)
            except Failure:
                if self._rewrite:
                    self.current_step.rewrite("will_output").to(actual_output)
                else:
                    raise

        if raises is not None:
            exception_type = raises.get("type")
            message = raises.get("message")

            try:
                result.exception_was_raised(exception_type)
                actual_exception_message = result.exception.message
                strings_match(message, actual_exception_message)
            except Failure:
                if self._rewrite:
                    new_raises = raises.copy()
                    new_raises["message"] = actual_exception_message
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
