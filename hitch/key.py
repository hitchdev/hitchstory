from commandlib import Command
from hitchstory import StoryCollection, BaseEngine, exceptions, validate
from hitchstory import GivenDefinition, GivenProperty, InfoDefinition, InfoProperty
from hitchrun import expected
from strictyaml import Str, Map, Optional, Enum
from pathquery import pathquery
from hitchrun import DIR
from hitchrunpy import ExamplePythonCode, HitchRunPyException
from hitchstory import no_stacktrace_for
from templex import Templex
import hitchpylibrarytoolkit
import dirtemplate
import colorama
import re


class Engine(BaseEngine):
    """Python engine for running tests."""

    given_definition = GivenDefinition(
        base_story=GivenProperty(Str()),
        example_story=GivenProperty(Str()),
        example1_story=GivenProperty(Str()),
        example2_story=GivenProperty(Str()),
        example3_story=GivenProperty(Str()),
        documentation_jinja2=GivenProperty(Str()),
        python_version=GivenProperty(Str()),
        engine_py=GivenProperty(Str()),
        setup=GivenProperty(Str()),
    )

    info_definition = InfoDefinition(
        status=InfoProperty(schema=Enum(["experimental", "stable"])),
        docs=InfoProperty(schema=Str()),
    )

    def __init__(self, paths, settings):
        self.path = paths
        self.settings = settings

    def set_up(self):
        """Set up the environment ready to run the stories."""
        self.path.state = self.path.gen.joinpath("state")

        if self.path.state.exists():
            self.path.state.rmtree(ignore_errors=True)
        self.path.state.mkdir()

        for mockfile in self.path.key.joinpath("mockcode").listdir():
            mockfile.copy(self.path.state)

        self.path.key.joinpath("code_that_does_things.py").copy(self.path.state)

        # hitchstory needs to be refactored to be able to clean up this repetition
        for filename in [
            "base.story",
            "example.story",
            "example1.story",
            "example2.story",
            "example3.story",
            "engine.py",
            "documentation.jinja2",
        ]:
            if filename in self.given:
                self.path.state.joinpath(filename).write_text(self.given[filename])

        self.python = hitchpylibrarytoolkit.project_build(
            "hitchstory", self.path, self.given.get("python_version", "3.7.0")
        ).bin.python

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
        )
        to_run = self.example_py_code.with_code(code)

        if self.settings.get("cprofile"):
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
                if self.settings.get("overwrite artefacts"):
                    self.current_step.update(**{"will output": actual_output})
                else:
                    raise

        if raises is not None:
            exception_type = raises.get("type")
            message = raises.get("message")

            try:
                result = self.example_py_code.expect_exceptions().run()
                result.exception_was_raised(exception_type)
                exception_message = self._story_friendly_output(
                    result.exception.message
                )
                Templex(exception_message).assert_match(message)
            except AssertionError:
                if self.settings.get("overwrite artefacts"):
                    new_raises = raises.copy()
                    new_raises["message"] = exception_message
                    self.current_step.update(raises=new_raises)
                else:
                    raise

    def example_story_unchanged(self):
        assert (
            self.path.state.joinpath("example.story").text()
            == self.given["example_story"]
        ), "example.story should have been unchanged but was changed"

    @no_stacktrace_for(AssertionError)
    def file_contents_will_be(self, filename, contents):
        file_contents = "\n".join(
            [
                line.rstrip()
                for line in self.path.state.joinpath(filename)
                .bytes()
                .decode("utf8")
                .strip()
                .split("\n")
            ]
        )
        try:
            Templex(contents.strip()).assert_match(file_contents)
        except AssertionError:
            if self.settings.get("overwrite artefacts"):
                self.current_step.update(contents=file_contents)
            else:
                raise

    def pause(self, message="Pause"):
        if hasattr(self, "services"):
            self.services.start_interactive_mode()
        import IPython

        IPython.embed()
        if hasattr(self, "services"):
            self.services.stop_interactive_mode()

    @no_stacktrace_for(FileNotFoundError)
    def output_is(self, expected_contents):
        Templex(self.path.state.joinpath("output.txt").text()).assert_match(
            expected_contents
        )
        self.path.state.joinpath("output.txt").remove()

    def splines_reticulated(self):
        assert self.path.state.joinpath("splines_reticulated.txt").exists()
        self.path.state.joinpath("splines_reticulated.txt").remove()

    def llamas_ass_kicked(self):
        assert self.path.state.joinpath("kicked_llamas_ass.txt").exists()
        self.path.state.joinpath("kicked_llamas_ass.txt").remove()

    def tear_down_was_run(self):
        assert self.path.state.joinpath("tear_down_was_run.txt").exists()
        self.path.state.joinpath("tear_down_was_run.txt").remove()

    def file_was_created_with(self, filename="", contents=""):
        if not self.path.state.joinpath(filename).exists():
            raise RuntimeError("{0} does not exist".format(filename))
        if self.path.state.joinpath(filename).bytes().decode("utf8") != contents:
            raise RuntimeError("{0} did not contain {0}".format(filename, contents))

    def form_filled(self, **kwargs):
        for name, value in kwargs.items():
            assert value == self.path.state.joinpath(
                "{0}.txt".format(name)
            ).bytes().decode("utf8")

    def buttons_clicked(self, contents):
        assert (
            contents.strip()
            == self.path.state.joinpath("buttons.txt").bytes().decode("utf8").strip()
        )


def _storybook(settings):
    return StoryCollection(pathquery(DIR.key).ext("story"), Engine(DIR, settings))


@expected(exceptions.HitchStoryException)
def rbdd(*keywords):
    """
    Run story with name containing keywords and rewrite.
    """
    _storybook({"overwrite artefacts": True, "print output": True}).shortcut(
        *keywords
    ).play()


@expected(exceptions.HitchStoryException)
def bdd(*keywords):
    """
    Run story with name containing keywords.
    """
    _storybook({"overwrite artefacts": False, "print output": True}).shortcut(
        *keywords
    ).play()


@expected(exceptions.HitchStoryException)
def regressfile(filename):
    """
    Run all stories in filename 'filename'.
    """
    StoryCollection(
        pathquery(DIR.key).ext("story"), Engine(DIR, {"overwrite artefacts": False})
    ).in_filename(filename).ordered_by_name().play()


@expected(exceptions.HitchStoryException)
def regression():
    """
    Continuos integration - lint and run all stories.
    """
    lint()
    StoryCollection(
        pathquery(DIR.key).ext("story"), Engine(DIR, {"overwrite artefacts": False})
    ).only_uninherited().ordered_by_name().play()


def reformat():
    """
    Reformat using black and then relint.
    """
    hitchpylibrarytoolkit.reformat(DIR.project, "hitchstory")


def lint():
    """
    Lint project code and hitch code.
    """
    hitchpylibrarytoolkit.lint(DIR.project, "hitchstory")


def deploy(version):
    """
    Deploy to pypi as specified version.
    """
    hitchpylibrarytoolkit.deploy(DIR.project, "hitchstory", version)


@expected(dirtemplate.exceptions.DirTemplateException)
def docgen():
    """
    Build documentation.
    """
    hitchpylibrarytoolkit.docgen(_storybook({}), DIR.project, DIR.key, DIR.gen)


@expected(dirtemplate.exceptions.DirTemplateException)
def readmegen():
    """
    Build documentation.
    """
    hitchpylibrarytoolkit.readmegen(
        _storybook({}), DIR.project, DIR.key, DIR.gen, "hitchstory"
    )


def rerun(version="3.7.0"):
    """
    Rerun last example code block with specified version of python.
    """
    Command(DIR.gen.joinpath("py{0}".format(version), "bin", "python"))(
        DIR.gen.joinpath("state", "examplepythoncode.py")
    ).in_dir(DIR.gen.joinpath("state")).run()
