from hitchstory import StoryCollection
from engine import Engine
from pathlib import Path

PROJECTDIR = Path(__file__).absolute().parents[0].parent

storydocs = (
    StoryCollection(PROJECTDIR.joinpath("story").glob("*.story"), Engine())
    .with_documentation(PROJECTDIR.joinpath("tests", "docstory.yml").read_text())
    .ordered_by_file()
)

for story in storydocs:
    PROJECTDIR.joinpath("docs", story.slug + ".md").write_text(story.documentation())
