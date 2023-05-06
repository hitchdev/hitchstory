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
from pathlib import Path
from shlex import split
from podman import App
from commandlib import Command
import requests
import time


PROJECT_DIR = Path(__file__).absolute().parents[0].parent


class Engine(BaseEngine):
    """Python engine for running tests."""

    def __init__(self, rewrite=False):
        self._app = App(Command("podman").in_dir(PROJECT_DIR))
        self._rewrite = rewrite

    def set_up(self):
        self._app.start()
        self._app.wait_until_ready()

    @validate(
        request=Map(
            {
                "path": Str(),
                "method": Str(),
                Optional("headers"): MapPattern(Str(), Str()),
            }
        ),
        response=Map(
            {
                "code": Int(),
            }
        ),
    )
    def call_api(self, request, response=None, request_content="", response_content=""):
        actual_response = requests.request(
            request["method"],
            "http://127.0.0.1:5000/" + request["path"],
            data=request_content,
            headers=request.get("headers", {}),
        )

        if response is not None:
            assert response["code"] == actual_response.status_code, (
                f"Response code was {actual_response.status_code}, "
                f"should be {response['code']}."
            )

        try:
            json_match(response_content, actual_response.text)
        except Failure:
            if self._rewrite:
                self.current_step.rewrite("response_content").to(
                    actual_response.text
                )
            else:
                raise

    def tear_down(self):
        self._app.stop()

    def on_failure(self, result):
        self._app.logs()

    def on_success(self):
        if self._rewrite:
            self.new_story.save()



collection = StoryCollection(
    Path(__file__).parent.parent.joinpath("story").glob("*.story"),
    Engine(rewrite=getenv("STORYMODE", "") == "rewrite"),
)

collection.with_external_test_runner().ordered_by_name().add_pytests_to(
    module=__import__(__name__)  # This module
)
