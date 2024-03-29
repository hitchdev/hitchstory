"""
Generates the markdown docs in docs/ using docstory.yml
and the YAML stories marked for documentation as the input.
"""

from pathlib import Path
from hitchstory import StoryCollection
from test_integration import Engine
import inflect

PROJECTDIR = Path(__file__).absolute().parents[0].parent

IENG = inflect.engine()


def ordinal(num):
    """0 -> first, 1 -> second, -1 -> last, etc."""
    if num >= 0:
        return IENG.number_to_words(IENG.ordinal(num + 1))
    elif num == -1:
        return "last"
    else:
        return "{} last".format(IENG.number_to_words(IENG.ordinal(num * -1)))


def generate_docs():
    storydocs = (
        StoryCollection(PROJECTDIR.joinpath("hitch", "story").glob("*.story"), Engine())
        .with_documentation(
            PROJECTDIR.joinpath("hitch", "docstory.yml").read_text(),
            extra={"ordinal": ordinal},
        )
        .filter(lambda story: story.info.get("docs"))
        .ordered_by_file()
    )

    for story in storydocs:
        PROJECTDIR.joinpath("hitch", "docs", story.slug + ".md").write_text(
            story.documentation()
        )


if __name__ == "__main__":
    generate_docs()
