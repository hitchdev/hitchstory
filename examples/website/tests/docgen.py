from pathlib import Path

from hitchstory import StoryCollection
from test_integration import Engine

PROJECTDIR = Path(__file__).absolute().parents[0].parent

storydocs = (
    StoryCollection(PROJECTDIR.joinpath("story").glob("*.story"), Engine())
    .with_documentation(PROJECTDIR.joinpath("tests", "docstory.yml").read_text())
    .ordered_by_file()
)

for story in storydocs:
    PROJECTDIR.joinpath("docs", story.slug + ".md").write_text(story.documentation())
