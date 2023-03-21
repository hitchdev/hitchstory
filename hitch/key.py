from hitchstory import StoryCollection
from commandlib import Command
from pathquery import pathquery
from click import argument, group, pass_context
from hitchpylibrarytoolkit.project_docs import ProjectDocumentation
import hitchpylibrarytoolkit
import pyenv
from path import Path
from engine import Engine


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


DIR = Directories()


toolkit = hitchpylibrarytoolkit.ProjectToolkitV2(
    "HitchStory",
    "hitchstory",
    "hitchdev/hitchstory",
)

DIR = toolkit.DIR


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
    ProjectDocumentation(
        _storybook(python_path=_devenv().python_path),
        DIR.project,
        DIR.project / "docs" / "draft",
        "HitchStory",
        "hitchdev/hitchstory",
        image="![](sliced-cucumber.jpg)",
    ).generate()


@cli.command()
def publishdocs():
    # ![](sliced-cucumber.jpg)
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

    ProjectDocumentation(
        _storybook(python_path=_devenv().python_path),
        DIR.project,
        DIR.project / "docs" / "public",
        "HitchStory",
        "hitchdev/hitchstory",
        image="![](sliced-cucumber.jpg)",
    ).generate()

    git("add", "docs/public").run()
    git("commit", "-m", "DOCS : Regenerated docs.").run()

    git("push").run()


@cli.command()
def readmegen():
    """
    Build documentation.
    """
    ProjectDocumentation(
        _storybook(python_path=_devenv().python_path),
        DIR.project,
        DIR.project / "docs" / "draft",
        "HitchStory",
        "hitchdev/hitchstory",
        image="![](sliced-cucumber.jpg)",
    ).generate(readme=True)
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

    prerequisites = [
        pyenv.PythonVersionDependentRequirement(
            package="markupsafe",
            lower_version="2.0.0",
            python_version_threshold="3.9",
            higher_version="2.1.2",
        ),
        pyenv.PythonRequirements(
            [
                "ensure",
            ]
        ),
    ]

    envirotest.run_test(
        pyenv.Pyenv(DIR.gen / "pyenv"),
        DIR.project.joinpath("pyproject.toml").text(),
        test_package,
        prerequisites,
        strategy_name,
        _storybook,
        lambda python_path: False,
    )


if __name__ == "__main__":
    cli()
