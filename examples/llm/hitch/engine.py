"""
This module contains the:

* Code that translates all of the YAML stories into pytest tests.
* Story Engine that interprets and validates the steps.
"""
from hitchstory import BaseEngine, InfoDefinition, InfoProperty
from hitchstory import GivenDefinition, GivenProperty
from strictyaml import CommaSeparated, Enum, Int, Str, MapPattern, Bool, Map, Int
from hitchstory import no_stacktrace_for, validate
from hitchstory import Failure, json_match
from commandlib import Command, python_bin
from directories import DIR
from slugify import slugify
from pathlib import Path
from llm import LLMClient, LLMServer, LLMAnswers
import nest_asyncio
import shutil
import json
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

    def __init__(self, rewrite=False, print_output=True):
        self._rewrite = rewrite
        self._print_output = print_output
        
    def _print(self, output):
        if self._print_output:
            print(output)
    
    def set_up(self):
        self._client = LLMClient(prompt=self.given["customer_instructions"])
        self._server = LLMServer(prompt=self.given["agent_instructions"])
        self._answers = LLMAnswers()
        self._print("")
    
    def expect_json(self, expected_json):
        client_question = self._client.run()
        self._print(f"CUSTOMER : {client_question}")
        server_response = self._server.run([{"role": "user", "content": client_question}])
        self._print(f"SERVER : {server_response}")
        json_match(server_response, expected_json)
        
    def expect_message(self, question, response):
        client_question = self._client.run()
        self._print(f"CUSTOMER : {client_question}")
        server_response = self._server.run([{"role": "user", "content": client_question}])
        message = json.loads(server_response)["message"]
        self._print(f"SERVER : {message}")
        answer_response = self._answers.ask(message, question)
        sanitized = answer_response.replace(".", "").lower()
        if response.lower() != sanitized:
            raise Failure(f"Expected {response}, got {answer_response}")
    
    def tear_down(self):
        pass
