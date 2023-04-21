from hitchstory import StoryCollection
from click import argument, group, pass_context
from commandlib import Command
from engine import Engine
from pathlib import Path

PROJECT_DIRECTORY = Path(__file__).absolute().parents[0].parent


class DIR:
    """All relevant directories"""

    key = PROJECT_DIRECTORY / "hitch"
    project = PROJECT_DIRECTORY
    story = PROJECT_DIRECTORY / "story"
    docs = PROJECT_DIRECTORY / "docs"
    gen = Path("/gen")


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
    Run story with name containing keywords and rewrite.
    """
    _storybook(rewrite=True).shortcut(*keywords).play()


@cli.command()
@argument("keywords", nargs=-1)
def atdd(keywords):
    """
    Run story with name containing keywords.
    """
    _storybook().shortcut(*keywords).play()


@cli.command()
def regression():
    """
    Run all child tests.
    """
    _storybook().only_uninherited().ordered_by_name().play()


@cli.command()
def docgen():
    """
    Generate documentation using docstory.yml templates.
    """
    storydocs = _storybook().with_documentation(
        DIR.project.joinpath("hitch", "docstory.yml").read_text()
    )

    for story in storydocs.ordered_by_file():
        DIR.docs.joinpath(story.slug + ".md").write_text(story.documentation())


@cli.command()
def build():
    if not Path("/gen/devenv").exists():
        Command("virtualenv", "/gen/devenv").run()
        Command("/gen/devenv/bin/pip", "install", "textblob").run()


if __name__ == "__main__":
    cli()
