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
from llm import LLMServer, LLMAnswers
import shutil
import json
import time
import sys


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
        self._server = LLMServer(prompt=self.given["agent_instructions"])
        self._answers = LLMAnswers()
        self._print("")
    
    @validate(expect_answer=Map({"question": Str(), "response": Str()}))
    def speak(self, message, expect_json=None, expect_answer=None):
        self._print(f"CUSTOMER : {message}")
        server_response = self._server.run([{"role": "user", "content": message}])
        self._print(f"SERVER : {server_response}")
        
        if expect_json is not None:
            try:
                json_match(server_response, expect_json)
            except Failure:
                if self._rewrite:
                    self.current_step.rewrite("expect_json").to(server_response)
                else:   
                    raise
        
        if expect_answer is not None:
            answer = json.loads(server_response)["message"]
            answer_response = self._answers.ask(answer, expect_answer["question"])
            sanitized = answer_response.replace(".", "").lower()
            response = expect_answer["response"]
            if response.lower() != sanitized:
                raise Failure(f"Expected {response}, got {answer_response}")
    
    def tear_down(self):
        pass
