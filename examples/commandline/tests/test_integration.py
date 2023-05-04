from hitchstory import StoryCollection
from pathlib import Path
from engine import Engine
from os import getenv


collection = StoryCollection(
    Path(__file__).parent.parent.joinpath("story").glob("*.story"),
    Engine(rewrite=getenv("MODE", "") == "rewrite"),
)

collection.with_external_test_runner().ordered_by_name().add_pytests_to(
    module=__import__(__name__)  # This module
)
