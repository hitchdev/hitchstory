"""
This module contains the:

* Code that translates all of the YAML stories into pytest tests.
* Story Engine that interprets and validates the steps.
"""
from hitchstory import BaseEngine, InfoDefinition, InfoProperty
from hitchstory import GivenDefinition, GivenProperty
from strictyaml import CommaSeparated, Enum, Int, Str, MapPattern, Bool, Map, Int
from hitchstory import no_stacktrace_for, validate
from commandlib import Command, python_bin
from directories import DIR
from slugify import slugify
from pathlib import Path
import nest_asyncio
import shutil
import time
import sys

# This allows the IPython REPL to play nicely with Playwright,
# since they both want an event loop.
# To pause and debug any code at any point in these modules, use
# __import__("IPython").embed()
nest_asyncio.apply()


class Engine(BaseEngine):
    """
    Python engine for validating, running and debugging YAML stories.
    """

    # StrictYAML schemas for metadata about the stories
    # See docs: https://hitchdev.com/hitchstory/using/engine/metadata/
    info_definition = InfoDefinition(
        context=InfoProperty(schema=Str()),
        jiras=InfoProperty(schema=CommaSeparated(Str())),
        docs=InfoProperty(schema=Bool()),
    )

    # StrictYAML schemas for given preconditions
    # See docs: https://hitchdev.com/hitchstory/using/engine/given/
    given_definition = GivenDefinition(
        agent_instructions=GivenProperty(Str()),
        customer_instructions=GivenProperty(Str()),
    )

    def __init__(self, rewrite=False):
        self._rewrite = rewrite
    
    def set_up(self):
        pass
    
    def run(self, expect_json):
        pass
    
    def tear_down(self):
        pass
