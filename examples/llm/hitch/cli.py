from hitchstory import StoryCollection
from click import argument, group, pass_context
from engine import Engine
from directories import DIR
from os import getenv


def _collection(**args):
    return StoryCollection(
        DIR.STORY.glob("*.story"),
        Engine(**args),
    )


@group(invoke_without_command=True)
@pass_context
def cli(ctx):
    """Integration test command line interface."""
    pass


@cli.command()
@argument("keywords", nargs=-1)
def rbdd(keywords):
    """
    Run story with name containing keywords and rewrite.
    """
    _collection(rewrite=True).shortcut(*keywords).play()


@cli.command()
@argument("keywords", nargs=-1)
def bdd(keywords):
    """
    Run story with name containing keywords.
    """
    _collection(rewrite=False).shortcut(*keywords).play()


@cli.command()
def regression():
    """
    Continuous integration - run all stories.
    """
    _collection(print_output=False).only_uninherited().ordered_by_name().play()


if __name__ == "__main__":
    cli()
