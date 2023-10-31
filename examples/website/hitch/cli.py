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
    _collection().shortcut(*keywords).play()


@cli.command()
@argument("keywords", nargs=-1)
def bdd(keywords):
    """
    Run story with name containing keywords.
    """
    _collection(rewrite=True).shortcut(*keywords).play()


@cli.command()
@argument("keywords", nargs=-1)
def vbdd(keywords):
    """
    Run story with name containing keywords.
    """
    _collection(vnc=True).shortcut(*keywords).play()


@cli.command()
def regression():
    """
    Continuos integration - lint and run all stories.
    """
    _collection().only_uninherited().ordered_by_name().play()


if __name__ == "__main__":
    cli()
