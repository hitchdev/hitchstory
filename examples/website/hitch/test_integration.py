"""
This module contains the:

* Code that translates all of the YAML stories into pytest tests.
"""
from engine import Engine
from hitchstory import StoryCollection
from directories import DIR
from os import getenv
from pathlib import Path


collection = StoryCollection(
    # Grab all stories from all *.story files in the story directory.
    DIR.STORY.glob("*.story"),
    Engine(
        rewrite=getenv("STORYMODE", "") == "rewrite",
        vnc=getenv("STORYMODE", "") == "vnc",
        coverage=getenv("STORYMODE", "") == "coverage",
        timeout=10.0,
    ),
)

# Turn all stories into pytest tests
collection.with_external_test_runner().only_uninherited().ordered_by_name().add_pytests_to(
    module=__import__(__name__)  # This module
)
