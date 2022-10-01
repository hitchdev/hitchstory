from commandlib import Command
from hitchstory import StoryCollection, BaseEngine, validate
from hitchstory import GivenDefinition, GivenProperty, InfoDefinition, InfoProperty
from strictyaml import Str, Map, Optional, Enum, MapPattern
from pathquery import pathquery
from click import argument, group, pass_context
from hitchrunpy import ExamplePythonCode, HitchRunPyException
from hitchstory import no_stacktrace_for
from templex import Templex
import hitchpylibrarytoolkit
import colorama
import re
from path import Path


class Directories:
    gen = Path("/gen")
    key = Path("/src/hitch/")
    project = Path("/src/")
    share = Path("/gen")


DIR = Directories()


@group(invoke_without_command=True)
@pass_context
def cli(ctx):
    """Integration test command line interface."""
    pass


class Directories:
    gen = Path("/gen")
    key = Path("/src/hitch/")
    project = Path("/src/")
    share = Path("/gen")


DIR = Directories()


toolkit = hitchpylibrarytoolkit.ProjectToolkit(
    "hitchstory",
    DIR,
)


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

    def __init__(self, paths, settings):
        self.path = paths
        self.settings = settings

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

        self.pylibrary = hitchpylibrarytoolkit.PyLibraryBuild(
            "hitchstory",
            self.path,
        ).with_python_version(self.given.get("python_version", "3.7.0"))
        self.pylibrary.ensure_built()
        self.python = self.pylibrary.bin.python

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
        Templex(self.path.working.joinpath("output.txt").text()).assert_match(
            expected_contents
        )
        self.path.working.joinpath("output.txt").remove()

    def splines_reticulated(self):
        assert self.path.working.joinpath("splines_reticulated.txt").exists()
        self.path.working.joinpath("splines_reticulated.txt").remove()

    def llamas_ass_kicked(self):
        assert self.path.working.joinpath("kicked_llamas_ass.txt").exists()
        self.path.working.joinpath("kicked_llamas_ass.txt").remove()

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

    def buttons_clicked(self, contents):
        assert (
            contents.strip()
            == self.path.working.joinpath("buttons.txt").bytes().decode("utf8").strip()
        )

    def tear_down(self):
        if self.path.q.exists():
            print(self.path.q.text())


def _storybook(settings):
    return StoryCollection(pathquery(DIR.key).ext("story"), Engine(DIR, settings))


@cli.command()
@argument("keywords", nargs=-1)
def rbdd(keywords):
    """
    Run story with name containing keywords and rewrite.
    """
    _storybook({"overwrite artefacts": True, "print output": True}).shortcut(
        *keywords
    ).play()


@cli.command()
@argument("keywords", nargs=-1)
def bdd(keywords):
    """
    Run story with name containing keywords.
    """
    _storybook({"overwrite artefacts": False, "print output": True}).shortcut(
        *keywords
    ).play()


@cli.command()
def regressfile(filename):
    """
    Run all stories in filename 'filename'.
    """
    StoryCollection(
        pathquery(DIR.key).ext("story"), Engine(DIR, {"overwrite artefacts": False})
    ).in_filename(filename).ordered_by_name().play()


@cli.command()
def rewriteall():
    """
    Run all stories in rewrite mode.
    """
    StoryCollection(
        pathquery(DIR.key).ext("story"), Engine(DIR, {"overwrite artefacts": True})
    ).only_uninherited().ordered_by_name().play()


@cli.command()
def regression():
    """
    Continuos integration - lint and run all stories.
    """
    # toolkit.lint(exclude=["__init__.py"])
    StoryCollection(
        pathquery(DIR.key).ext("story"), Engine(DIR, {"overwrite artefacts": False})
    ).only_uninherited().ordered_by_name().play()


@cli.command()
def reformat():
    """
    Reformat using black and then relint.
    """
    toolkit.reformat()


@cli.command()
def lint():
    """
    Lint project code and hitch code.
    """
    toolkit.lint(exclude=["__init__.py"])


@cli.command()
def deploy(version):
    """
    Deploy to pypi as specified version.
    """
    toolkit.deploy(version)


@cli.command()
def docgen():
    """
    Build documentation.
    """
    toolkit.docgen(Engine(DIR, {}))


@cli.command()
def readmegen():
    """
    Build documentation.
    """
    toolkit.readmegen(Engine(DIR, {}))


@cli.command()
def rerun(version="3.7.0"):
    """
    Rerun last example code block with specified version of python.
    """
    Command(DIR.gen.joinpath("py{0}".format(version), "bin", "python"))(
        DIR.gen.joinpath("state", "examplepythoncode.py")
    ).in_dir(DIR.gen.joinpath("state")).run()


if __name__ == "__main__":
    cli()
