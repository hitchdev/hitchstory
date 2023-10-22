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
from commandlib import Command
import requests
import time
from podman import App
import json
from directories import DIR

PROJECT_DIR = Path(__file__).absolute().parents[0].parent


class Engine(BaseEngine):
    """Python engine for running tests."""

    def __init__(self, rewrite=False):
        self._app = App(Command("podman").in_dir(DIR.PROJECT))
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
                Optional("content"): Str(),
            }
        ),
        response=Map(
            {
                Optional("code"): Int(),
                "content": Str(),
                Optional("varying"): MapPattern(Str(), Enum(["uuid", "timestamp"])),
            }
        ),
    )
    def call_api(self, request, response):
        actual_response = requests.request(
            request["method"],
            "http://127.0.0.1:5000/" + request["path"],
            data=request.get("content", ""),
            headers=request.get("headers", {}),
        )

        if "code" in response:
            if actual_response.status_code != response["code"]:
                raise Failure(
                    f"Response code was {actual_response.status_code}, "
                    f"should be {response['code']}"
                )

        json_actual_response = json.loads(actual_response.content)
        json_expected_response = json.loads(response["content"])
        for varying_key, varying_type in response.get("varying", {}).items():
            *other_keys, last_key = varying_key.split("/")

            actual_chunk = json_actual_response
            expected_chunk = json_expected_response

            for key in other_keys:
                actual_chunk = actual_chunk[key]
                expected_chunk = expected_chunk[key]

            if last_key in actual_chunk:
                expected_chunk[last_key] = actual_chunk[last_key]

        expected = json.dumps(json_expected_response, indent=4, sort_keys=True)

        try:
            json_match(expected, actual_response.text)
        except Failure:
            if self._rewrite:
                self.current_step.rewrite("response", "content").to(
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
