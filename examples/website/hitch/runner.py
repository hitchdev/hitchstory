from hitchstory import StoryCollection, HitchStoryException
from click import argument, group, pass_context, echo
from commandlib import Command, python_bin
from engine import Engine
from pathlib import Path
from sys import exit


PROJECT_DIRECTORY = Path(__file__).absolute().parents[0].parent


class DIR:
    """All relevant directories"""

    key = PROJECT_DIRECTORY / "hitch"
    project = PROJECT_DIRECTORY
    story = PROJECT_DIRECTORY / "story"
    docs = PROJECT_DIRECTORY / "docs"


@group(invoke_without_command=True)
@pass_context
def cli(ctx):
    """Integration test command line interface."""
    pass


def _storybook(**settings):
    """Get all stories available to run with settings (e.g. rewriting)"""
    return StoryCollection(DIR.story.glob("*.story"), Engine(DIR, **settings))


@cli.command()
@argument("keywords", nargs=-1)
def ratdd(keywords):
    """
    Run story with name containing keywords in rewrite mode.
    """
    _storybook(rewrite=True, recordings=True).shortcut(*keywords).play()


@cli.command()
@argument("keywords", nargs=-1)
def atdd(keywords):
    """
    Run story with name containing keywords.
    """
    try:
        _storybook().shortcut(*keywords).play()
    except HitchStoryException as error:
        echo(error)
        exit(1)


@cli.command()
def regression():
    """
    Run all child tests.
    """
    _storybook().only_uninherited().ordered_by_name().play()


@cli.command()
def recordings():
    """
    Regenerate screenshot and videos for use in docs.
    """
    _storybook(recordings=True).only_uninherited().ordered_by_name().play()


@cli.command()
def docgen():
    """
    Generate documentation using docstory.yml templates.
    """
    storydocs = _storybook().with_documentation(
        DIR.project.joinpath("hitch", "docstory.yml").read_text()
    )

    print("Generating")
    for story in storydocs.ordered_by_file():
        DIR.docs.joinpath(story.slug + ".md").write_text(story.documentation())
    print("Done")


@cli.command()
def build():
    """Build app and playwright server container."""
    Command("podman", "build", ".", "-t", "app").in_dir(DIR.project).run()
    Command(
        "podman", "build", "-f", "hitch/Dockerfile-playwright", "-t", "playwright"
    ).in_dir(DIR.project).run()


if __name__ == "__main__":
    cli()
