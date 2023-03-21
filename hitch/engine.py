from hitchstory import StoryCollection, BaseEngine, validate
from hitchstory import GivenDefinition, GivenProperty, InfoDefinition, InfoProperty
from strictyaml import Str, Map, Optional, Enum, MapPattern
from hitchstory import no_stacktrace_for
from hitchrunpy import ExamplePythonCode, HitchRunPyException
from commandlib import Command
from templex import Templex
from path import Path
import colorama
import re


class Engine(BaseEngine):
    """Python engine for running tests."""

    given_definition = GivenDefinition(
        files=GivenProperty(MapPattern(Str(), Str())),
        core_files=GivenProperty(MapPattern(Str(), Str())),
        python_version=GivenProperty(Str()),
        setup=GivenProperty(Str()),
    )

    info_definition = InfoDefinition(
        status=InfoProperty(schema=Enum(["experimental", "stable"])),
        docs=InfoProperty(schema=Str()),
    )

    def __init__(self, paths, python_path, rewrite=False, cprofile=False):
        self.path = paths
        self._rewrite = rewrite
        self._python_path = python_path
        self._cprofile = cprofile

    def set_up(self):
        """Set up the environment ready to run the stories."""
        self.path.q = Path("/tmp/q")
        self.path.state = self.path.gen.joinpath("state")
        self.path.working = self.path.state / "working"

        if self.path.q.exists():
            self.path.q.remove()
        if self.path.state.exists():
            self.path.state.rmtree(ignore_errors=True)
        self.path.state.mkdir()

        for mockfile in self.path.key.joinpath("mockcode").listdir():
            mockfile.copy(self.path.state)

        self.path.key.joinpath("code_that_does_things.py").copy(self.path.state)
        self._included_files = [self.path.key.joinpath("code_that_does_things.py")]

        for filename, contents in list(self.given.get("files", {}).items()):
            self.path.state.joinpath(filename).write_text(self.given["files"][filename])
            self._included_files.append(self.path.state.joinpath(filename))

        for filename, contents in list(self.given.get("core files", {}).items()):
            self.path.state.joinpath(filename).write_text(
                self.given["core files"][filename]
            )
            self._included_files.append(self.path.state.joinpath(filename))

        for filename in self.path.key.joinpath("mockcode").listdir():
            self._included_files.append(filename)

        self.python = Command(self._python_path)

    def _story_friendly_output(self, output):
        """
        Takes output from exceptions and to the screen that contains:

        * Environment specific paths.
        * Terminal color codes.
        * Random hexadecimal numbers.
        * Slightly longer lasting stories reporting 0.2  or shorted reporting 0.0 seconds.
        * Trailing spaces (these look screwy in YAML).

        ...and replaces them with a deterministic, representative or
        more human readable output.
        """
        friendly_output = "\n".join(
            [
                line.rstrip()
                for line in output.replace(colorama.Fore.RED, "[[ RED ]]")
                .replace(colorama.Style.BRIGHT, "[[ BRIGHT ]]")
                .replace(colorama.Style.DIM, "[[ DIM ]]")
                .replace(colorama.Fore.RESET, "[[ RESET FORE ]]")
                .replace(colorama.Style.RESET_ALL, "[[ RESET ALL ]]")
                .replace(self.path.state, "/path/to")
                .replace(self.path.gen, "/path/to/virtualenv")
                .replace("0.5 seconds", "0.1 seconds")
                .replace("0.4 seconds", "0.1 seconds")
                .replace("0.3 seconds", "0.1 seconds")
                .replace("0.2 seconds", "0.1 seconds")
                .replace("0.0 seconds", "0.1 seconds")
                .rstrip()
                .split("\n")
            ]
        )
        return re.sub(r"0x[0-9a-f]+", "0xfffffffffff", friendly_output)

    @no_stacktrace_for(AssertionError)
    @no_stacktrace_for(HitchRunPyException)
    @validate(
        code=Str(),
        will_output=Str(),
        raises=Map({Optional("type"): Str(), Optional("message"): Str()}),
    )
    def run(self, code, will_output=None, raises=None):
        self.example_py_code = (
            ExamplePythonCode(self.python, self.path.state)
            .with_terminal_size(160, 100)
            .with_setup_code(self.given.get("setup", ""))
            .include_files(*self._included_files)
        )
        to_run = self.example_py_code.with_code(code)

        if self._cprofile:
            to_run = to_run.with_cprofile(
                self.path.profile.joinpath("{0}.dat".format(self.story.slug))
            )

        result = (
            to_run.expect_exceptions().run() if raises is not None else to_run.run()
        )

        actual_output = self._story_friendly_output(result.output)

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
                exception_message = self._story_friendly_output(
                    result.exception.message
                )
                Templex(message).assert_match(exception_message)
            except AssertionError:
                if self._rewrite:
                    new_raises = raises.copy()
                    new_raises["message"] = exception_message
                    self.current_step.update(raises=new_raises)
                else:
                    raise

    def example_story_unchanged(self):
        assert (
            self.path.state.joinpath("example.story").text()
            == self.given["core files"]["example.story"]
        ), "example.story should have been unchanged but was changed"

    @no_stacktrace_for(AssertionError)
    def file_contents_will_be(self, filename, contents):
        file_contents = "\n".join(
            [
                line.rstrip()
                for line in self.path.working.joinpath(filename)
                .bytes()
                .decode("utf8")
                .strip()
                .split("\n")
            ]
        )
        try:
            Templex(contents.strip()).assert_match(file_contents)
        except AssertionError:
            if self._rewrite:
                self.current_step.update(contents=file_contents)
            else:
                raise

    def pause(self, message="Pause"):
        import IPython

        IPython.embed()

    @no_stacktrace_for(FileNotFoundError)
    def output_is(self, expected_contents):
        Templex(self.path.working.joinpath("output.txt").text()).assert_match(
            expected_contents
        )
        self.path.working.joinpath("output.txt").remove()

    def tear_down_was_run(self):
        assert self.path.working.joinpath("tear_down_was_run.txt").exists()
        self.path.working.joinpath("tear_down_was_run.txt").remove()

    def file_was_created_with(self, filename="", contents=""):
        if not self.path.working.joinpath(filename).exists():
            raise RuntimeError("{0} does not exist".format(filename))
        if self.path.working.joinpath(filename).bytes().decode("utf8") != contents:
            raise RuntimeError("{0} did not contain {1}".format(filename, contents))

    def form_filled(self, **kwargs):
        for name, value in kwargs.items():
            assert value == self.path.working.joinpath(
                "{0}.txt".format(name)
            ).bytes().decode("utf8")

    def tear_down(self):
        if self.path.q.exists():
            print(self.path.q.text())
