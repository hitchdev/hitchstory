from subprocess import call
from os import path
from commandlib import run, Command, CommandError
import hitchpython
import hitchserve
from hitchstory import StoryCollection, StorySchema, BaseEngine, exceptions, validate
from hitchrun import expected
import strictyaml
from strictyaml import MapPattern, Str, Seq, Map, Optional
from pathquery import pathq
import hitchtest
import hitchdoc
from simex import DefaultSimex
from commandlib import python
from hitchrun import hitch_maintenance
from hitchrun import DIR
from hitchrunpy import ExamplePythonCode, ExpectedExceptionMessageWasDifferent, HitchRunPyException
from hitchstory import expected_exception


class Engine(BaseEngine):
    """Python engine for running tests."""

    schema = StorySchema(
        preconditions=Map({
            Optional("files"): MapPattern(Str(), Str()), # TODO : remove
            Optional("base.story"): Str(),
            Optional("example.story"): Str(),
            Optional("example1.story"): Str(),
            Optional("example2.story"): Str(),
            Optional("engine.py"): Str(),
            Optional("setup"): Str(),
            Optional("code"): Str(),
        }),
        about={
            Optional("tags"): Seq(Str()),
        },
    )

    def __init__(self, paths, settings):
        self.path = paths
        self.settings = settings

    def set_up(self):
        """Set up your applications and the test environment."""
        self.path.state = self.path.gen.joinpath("state")

        self.doc = hitchdoc.Recorder(
            hitchdoc.HitchStory(self),
            self.path.gen.joinpath('storydb.sqlite'),
        )

        if self.path.state.exists():
            self.path.state.rmtree(ignore_errors=True)
        self.path.state.mkdir()
        self.path.key.joinpath("code_that_does_things.py").copy(self.path.state)
        
        for filename in ["example.story", "example1.story", "example2.story", "engine.py", ]:
            if filename in self.preconditions:
                self.path.state.joinpath(filename).write_text(self.preconditions[filename])
        

        for filename, text in self.preconditions.get("files", {}).items():
            filepath = self.path.state.joinpath(filename)
            if not filepath.dirname().exists():
                filepath.dirname().mkdir()
            filepath.write_text(text)

        self.python_package = hitchpython.PythonPackage(
            self.preconditions.get('python_version', '3.5.0')
        )
        self.python_package.build()

        self.pip = self.python_package.cmd.pip
        self.python = self.python_package.cmd.python

        # Install debugging packages
        with hitchtest.monitor([self.path.key.joinpath("debugrequirements.txt")]) as changed:
            if changed:
                run(self.pip("install", "-r", "debugrequirements.txt").in_dir(self.path.key))

        # Uninstall and reinstall
        with hitchtest.monitor(
            pathq(self.path.project.joinpath("hitchstory")).ext("py")
        ) as changed:
            if changed:
                self.pip("uninstall", "hitchstory", "-y").ignore_errors().run()
                self.pip("install", ".").in_dir(self.path.project).run()
    
    @expected_exception(HitchRunPyException)
    def run_code(self, expect_output=None):
        result = example_python_code = ExamplePythonCode(
            self.preconditions['code']
        ).with_setup_code(self.preconditions.get('setup', ''))\
         .run(self.path.state, self.python)
        print(result.output)

    def long_form_exception_raised(self, artefact=None):
        try:
            self.result = ExamplePythonCode(
                self.preconditions['code']
            ).with_setup_code(self.preconditions.get('setup', ''))\
             .expect_exceptions()\
             .run(self.path.state, self.python)
            processed_message = self.result.exception.message.replace(self.path.state, "/path/to")
            assert processed_message == self.path.key.joinpath(
                "artefacts", "{0}.txt".format(artefact.replace(" ", "-").lower())
            ).bytes().decode('utf8')
        except AssertionError:
            if self.settings.get("overwrite artefacts"):
                self.path.key.joinpath(
                    "artefacts", "{0}.txt".format(artefact.replace(" ", "-").lower())
                ).write_text(processed_message)
    
    def raises_exception(self, message=None, exception_type=None):
        try:
            self.result = ExamplePythonCode(
                self.preconditions['code']
            ).with_setup_code(self.preconditions.get('setup', ''))\
             .expect_exceptions()\
             .run(self.path.state, self.python)
           
            import re
            self.result.exception_was_raised(exception_type=exception_type)
            processed_message = self.result.exception.message.replace(self.path.state, "/path/to")
            processed_message = re.compile(r'0x[0-9a-f]+').sub("0xffffffff", processed_message)
            assert message == processed_message
        except AssertionError:
            if self.settings.get("overwrite artefacts"):
                self.current_step.update(message=processed_message)

    def code(self, command):
        self.doc.step("code", command=command)


    def returns_true(self, command, why=''):
        self.ipython_step_library.assert_true(command)
        self.doc.step("true", command=command, why=why)

    def assert_true(self, command):
        self.ipython_step_library.assert_true(command)
        self.doc.step("true", command=command)

    def assert_exception(self, command, exception):
        assert exception.strip() in error
        self.doc.step("exception", command=command, exception=exception)

    def on_failure(self, result):
        if self.settings.get("pause_on_failure", True):
            if self.preconditions.get("launch_shell", False):
                self.services.log(message=self.stacktrace.to_template())

    def file_contents_will_be(self, filename, contents):
        assert self.path.state.joinpath(filename).bytes().decode('utf8').strip() == contents.strip()
        self.doc.step("filename contains", filename=filename, contents=contents)

    def pause(self, message="Pause"):
        if hasattr(self, 'services'):
            self.services.start_interactive_mode()
        import IPython
        IPython.embed()
        if hasattr(self, 'services'):
            self.services.stop_interactive_mode()

    @expected_exception(FileNotFoundError)
    def output_is(self, expected_contents):
        output_contents = self.path.state.joinpath("output.txt").bytes().decode('utf8').strip()
        regex = DefaultSimex(
            open_delimeter="(((",
            close_delimeter=")))",
            exact=True,
        ).compile(expected_contents.strip())
        if regex.match(output_contents) is None:
            raise RuntimeError("Expected output:\n{0}\n\nActual output:\n{1}".format(
                expected_contents,
                output_contents,
            ))
        self.path.state.joinpath("output.txt").remove()

    def output_contains(self, expected_contents):
        output_contents = self.path.state.joinpath("output.txt").bytes().decode('utf8').strip()
        regex = DefaultSimex(
            open_delimeter="(((",
            close_delimeter=")))",
        ).compile(expected_contents.strip())
        if regex.search(output_contents) is None:
            raise RuntimeError("Expected to find:\n{0}\n\nActual output:\n{1}".format(
                expected_contents,
                output_contents,
            ))
        self.path.state.joinpath("output.txt").remove()

    @validate(changeable=Seq(Str()))
    def output_will_be(self, reference, changeable=None):
        output_contents = self.path.state.joinpath("output.txt").bytes().decode('utf8').strip()

        artefact = self.path.key.joinpath(
            "artefacts", "{0}.txt".format(reference.replace(" ", "-").lower())
        )

        simex = DefaultSimex(
            open_delimeter="(((",
            close_delimeter=")))",
        )

        simex_contents = output_contents

        if changeable is not None:
            for replacement in changeable:
                simex_contents = simex.compile(replacement).sub(replacement, simex_contents)

        if not artefact.exists():
            artefact.write_text(simex_contents)
        else:
            if self.settings.get('overwrite artefacts'):
                artefact.write_text(simex_contents)
                #print(output_contents)
            else:
                if simex.compile(artefact.bytes().decode('utf8')).match(output_contents) is None:
                    raise RuntimeError("Expected to find:\n{0}\n\nActual output:\n{1}".format(
                        artefact.bytes().decode('utf8'),
                        output_contents,
                    ))
                #else:
                    #print(output_contents)

    def splines_reticulated(self):
        assert self.path.state.joinpath("splines_reticulated.txt").exists()
        self.path.state.joinpath("splines_reticulated.txt").remove()

    def llamas_ass_kicked(self):
        assert self.path.state.joinpath("kicked_llamas_ass.txt").exists()
        self.path.state.joinpath("kicked_llamas_ass.txt").remove()

    def file_was_created_with(self, filename="", contents=""):
        if not self.path.state.joinpath(filename).exists():
            raise RuntimeError("{0} does not exist".format(filename))
        if self.path.state.joinpath(filename).bytes().decode('utf8') != contents:
            raise RuntimeError("{0} did not contain {0}".format(filename, contents))

    def exception_raised(self, command, reference, changeable=None):
        result = self.ipython_step_library.run(command, swallow_exception=True).error
        assert result is not None
        self.path.state.joinpath("output.txt").write_text(result)
        self.output_will_be(reference, changeable)
      
    def on_success(self):
        self.new_story.save()

    def tear_down(self):
        try:
            self.shutdown_connection()
        except:
            pass
        if hasattr(self, 'services'):
            self.services.shutdown()


@expected(exceptions.HitchStoryException)
def tdd(*words):
    """
    Run test with words.
    """
    print(
        StoryCollection(
            pathq(DIR.key).ext("story"), Engine(DIR, {"overwrite artefacts": True})
        ).shortcut(*words).play().report()
    )


@expected(exceptions.HitchStoryException)
def testfile(filename):
    """
    Run all stories in filename 'filename'.
    """
    print(
        StoryCollection(
            pathq(DIR.key).ext("story"), Engine(DIR, {"overwrite artefacts": True})
        ).in_filename(filename).ordered_by_name().play().report()
    )


@expected(exceptions.HitchStoryException)
def regression():
    """
    Continuos integration - run all tests and linter.
    """
    lint()
    print(
        StoryCollection(
            pathq(DIR.key).ext("story"), Engine(DIR, {})
        ).ordered_by_name().play().report()
    )

@expected(CommandError)
def lint():
    """
    Lint all code.
    """
    python("-m", "flake8")(
        DIR.project.joinpath("hitchstory"),
        "--max-line-length=100",
        "--exclude=__init__.py",
    ).run()
    #python("-m", "flake8")(
        #DIR.key.joinpath("key.py"),
        #"--max-line-length=100",
        #"--exclude=__init__.py",
    #).run()
    print("Lint success!")


def hitch(*args):
    """
    Use 'h hitch --help' to get help on these commands.
    """
    hitch_maintenance(*args)


def deploy(version):
    """
    Deploy to pypi as specified version.
    """
    NAME = "hitchstory"
    git = Command("git").in_dir(DIR.project)
    version_file = DIR.project.joinpath("VERSION")
    old_version = version_file.bytes().decode('utf8')
    if version_file.bytes().decode("utf8") != version:
        DIR.project.joinpath("VERSION").write_text(version)
        git("add", "VERSION").run()
        git("commit", "-m", "RELEASE: Version {0} -> {1}".format(
            old_version,
            version
        )).run()
        git("push").run()
        git("tag", "-a", version, "-m", "Version {0}".format(version)).run()
        git("push", "origin", version).run()
    else:
        git("push").run()

    # Set __version__ variable in __init__.py, build sdist and put it back
    initpy = DIR.project.joinpath(NAME, "__init__.py")
    original_initpy_contents = initpy.bytes().decode('utf8')
    initpy.write_text(
        original_initpy_contents.replace("DEVELOPMENT_VERSION", version)
    )
    python("setup.py", "sdist").in_dir(DIR.project).run()
    initpy.write_text(original_initpy_contents)

    # Upload to pypi
    python(
        "-m", "twine", "upload", "dist/{0}-{1}.tar.gz".format(NAME, version)
    ).in_dir(DIR.project).run()


def docgen():
    """
    Generate documentation.
    """
    docpath = DIR.project.joinpath("docs")

    if not docpath.exists():
        docpath.mkdir()

    documentation = hitchdoc.Documentation(
        DIR.gen.joinpath('storydb.sqlite'),
        'doctemplates.yml'
    )

    for story in documentation.stories:
        story.write(
            "rst",
            docpath.joinpath("{0}.rst".format(story.slug))
        )


def rerun(version="3.5.0"):
    """
    Rerun last example code block with specified version of python.
    """
    Command(DIR.gen.joinpath("py{0}".format(version), "bin", "python"))(
        DIR.gen.joinpath("state", "examplepythoncode.py")
    ).in_dir(DIR.gen.joinpath("state")).run()
