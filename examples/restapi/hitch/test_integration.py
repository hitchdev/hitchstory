from os import getenv
from hitchstory import (
    StoryCollection,
    BaseEngine,
    exceptions,
    validate,
    no_stacktrace_for,
)
from hitchstory import GivenDefinition, GivenProperty, InfoDefinition, InfoProperty
from hitchstory import Failure, json_match
from strictyaml import Optional, Str, Map, Int, Bool, Enum, load, MapPattern
from shlex import split
from podman import App
from commandlib import Command
import requests
import time
import json
from engine import Engine
from directories import DIR


collection = StoryCollection(
    DIR.STORY.glob("*.story"),
    Engine(rewrite=getenv("STORYMODE", "") == "rewrite"),
)

collection.with_external_test_runner().ordered_by_name().add_pytests_to(
    module=__import__(__name__)  # This module
)
