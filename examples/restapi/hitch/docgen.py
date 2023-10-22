from hitchstory import StoryCollection
from test_integration import Engine
from directories import DIR


storydocs = (
    StoryCollection(DIR.STORY.glob("*.story"), Engine())
    .with_documentation(DIR.TESTS.joinpath("docstory.yml").read_text())
    .ordered_by_file()
)

for story in storydocs:
    DIR.DOCS.joinpath(story.slug + ".md").write_text(story.documentation())
