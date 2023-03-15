from commandlib import Command
from hitchstory import StoryCollection, BaseEngine, validate
from hitchstory import GivenDefinition, GivenProperty, InfoDefinition, InfoProperty
from strictyaml import Str, Map, Optional, Enum, MapPattern
from pathquery import pathquery
from click import argument, group, pass_context
from hitchrunpy import ExamplePythonCode, HitchRunPyException
from hitchstory import no_stacktrace_for
from docgen import run_docgen
from templex import Templex
import hitchpylibrarytoolkit
import colorama
import re
import pyenv
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


def _storybook(**settings):
    return StoryCollection(pathquery(DIR.key).ext("story"), Engine(DIR, **settings))


def _current_version():
    return DIR.project.joinpath("VERSION").text().rstrip()


def _devenv():
    env = pyenv.DevelopmentVirtualenv(
        pyenv.Pyenv(DIR.gen / "pyenv"),
        DIR.project.joinpath("hitch", "devenv.yml"),
        DIR.project.joinpath("hitch", "debugrequirements.txt"),
        DIR.project,
        DIR.project.joinpath("pyproject.toml").text(),
    )
    env.ensure_built()
    return env


@cli.command()
@argument("keywords", nargs=-1)
def rbdd(keywords):
    """
    Run story with name containing keywords and rewrite.
    """
    _storybook(python_path=_devenv().python_path, rewrite=True).shortcut(
        *keywords
    ).play()


@cli.command()
@argument("keywords", nargs=-1)
def bdd(keywords):
    """
    Run story with name containing keywords.
    """
    _storybook(python_path=_devenv().python_path).shortcut(*keywords).play()


@cli.command()
@argument("filename")
def regressfile(filename):
    """
    Run all stories in filename 'filename'.
    """
    StoryCollection(
        pathquery(DIR.key).ext("story"), Engine(DIR, python_path=_devenv().python_path)
    ).in_filename(filename).ordered_by_name().play()


@cli.command()
def rewriteall():
    """
    Run all stories in rewrite mode.
    """
    StoryCollection(
        pathquery(DIR.key).ext("story"),
        Engine(DIR, python_path=_devenv().python_path, rewrite=True),
    ).only_uninherited().ordered_by_name().play()


@cli.command()
def regression():
    """
    Continuos integration - lint and run all stories.
    """
    # toolkit.lint(exclude=["__init__.py"])
    StoryCollection(
        pathquery(DIR.key).ext("story"), Engine(DIR, python_path=_devenv().python_path)
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
@argument("test", nargs=1)
def deploy(test="notest"):
    """
    Deploy to pypi as specified version.
    """
    from commandlib import python

    git = Command("git")

    if DIR.gen.joinpath("hitchstory").exists():
        DIR.gen.joinpath("hitchstory").rmtree()

    git("clone", "git@github.com:hitchdev/hitchstory.git").in_dir(DIR.gen).run()
    project = DIR.gen / "hitchstory"
    version = project.joinpath("VERSION").text().rstrip()
    initpy = project.joinpath("hitchstory", "__init__.py")
    original_initpy_contents = initpy.bytes().decode("utf8")
    initpy.write_text(original_initpy_contents.replace("DEVELOPMENT_VERSION", version))
    python("-m", "pip", "wheel", ".", "-w", "dist").in_dir(project).run()
    python("-m", "build", "--sdist").in_dir(project).run()
    initpy.write_text(original_initpy_contents)

    # Upload to pypi
    wheel_args = ["-m", "twine", "upload"]
    if test == "test":
        wheel_args += ["--repository", "testpypi"]
    wheel_args += ["dist/{}-{}-py3-none-any.whl".format("hitchstory", version)]

    python(*wheel_args).in_dir(project).run()

    sdist_args = ["-m", "twine", "upload"]
    if test == "test":
        sdist_args += ["--repository", "testpypi"]
    sdist_args += ["dist/{0}-{1}.tar.gz".format("hitchstory", version)]
    python(*sdist_args).in_dir(project).run()

    # Clean up
    DIR.gen.joinpath("hitchstory").rmtree()


@cli.command()
def draftdocs():
    """
    Build documentation.
    """
    run_docgen(DIR, _storybook({}))


@cli.command()
def publishdocs():
    if DIR.gen.joinpath("hitchstory").exists():
        DIR.gen.joinpath("hitchstory").rmtree()

    Path("/root/.ssh/known_hosts").write_text(
        Command("ssh-keyscan", "github.com").output()
    )
    Command("git", "clone", "git@github.com:hitchdev/hitchstory.git").in_dir(
        DIR.gen
    ).run()

    git = Command("git").in_dir(DIR.gen / "hitchstory")
    git("config", "user.name", "Bot").run()
    git("config", "user.email", "bot@hitchdev.com").run()
    git("rm", "-r", "docs/public").run()

    run_docgen(DIR, _storybook({}), publish=True)

    git("add", "docs/public").run()
    git("commit", "-m", "DOCS : Regenerated docs.").run()

    git("push").run()


@cli.command()
def readmegen():
    """
    Build documentation.
    """
    run_docgen(DIR, _storybook({}), readme=True)
    DIR.project.joinpath("docs", "draft", "index.md").copy("README.md")
    DIR.project.joinpath("docs", "draft", "changelog.md").copy("CHANGELOG.md")


@cli.command()
def build():
    _devenv()


@cli.command()
def cleanpyenv():
    pyenv.Pyenv(DIR.gen / "pyenv").clean()


@cli.command()
def cleandevenv():
    DIR.gen.joinpath("pyenv", "versions", "devvenv").remove()


@cli.command()
@argument("strategy_name", nargs=1)
def envirotest(strategy_name):
    """Run tests on package / python version combinations."""
    import envirotest
    import pyenv

    test_package = pyenv.PythonRequirements(
        [
            "hitchstory=={}".format(_current_version()),
        ],
        test_repo=True,
    )

    test_package = pyenv.PythonProjectDirectory(DIR.project)

    envirotest.run_test(
        pyenv.Pyenv(DIR.gen / "pyenv"),
        DIR.project.joinpath("pyproject.toml").text(),
        test_package,
        strategy_name,
        _storybook,
        lambda python_path: False,
    )


if __name__ == "__main__":
    cli()
