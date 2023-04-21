from hitchstory import (
    StoryCollection,
    BaseEngine,
    exceptions,
    validate,
    no_stacktrace_for,
)
from hitchstory import GivenDefinition, GivenProperty, InfoDefinition, InfoProperty
from templex import Templex
from strictyaml import Optional, Str, Map, Int, Bool, Enum, load, MapPattern
from path import Path
from shlex import split
from templex import Templex
from commandlib import Command
import requests
import time


class App:
    """Interact directly with the app via podman."""

    def __init__(self, podman):
        self._podman = podman

    def start(self):
        self._podman("run", "-d", "app").output()

    def wait_until_ready(self):
        # Really bad way to do it
        time.sleep(1)

    def stop(self):
        self._podman("stop", "--latest", "--time", "1").output()

    def logs(self):
        self._podman("logs", "--latest").run()


class Engine(BaseEngine):
    """Python engine for running tests."""

    def __init__(self, paths, rewrite=False):
        self._path = paths
        self._app = App(Command("podman").in_dir(self._path.project))
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
            Templex(response_content).assert_match(actual_response.text)
        except AssertionError:
            if self._rewrite:
                self.current_step.update(response_content=actual_response.text)
            else:
                raise

    def tear_down(self):
        self._app.stop()

    def on_failure(self, result):
        self._app.logs()

    def on_success(self):
        if self._rewrite:
            self.new_story.save()
