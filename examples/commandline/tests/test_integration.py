from os import getenv
from pathlib import Path

from commandlib import Command
from hitchstory import (
    BaseEngine,
    Failure,
    GivenDefinition,
    GivenProperty,
    InfoDefinition,
    InfoProperty,
    StoryCollection,
    no_stacktrace_for,
    strings_match,
)
from icommandlib import ICommand, IProcessTimeout
from strictyaml import Str

PROJECT_DIRECTORY = Path(__file__).absolute().parents[0].parent


class Engine(BaseEngine):
    """Python engine for running tests."""

    def __init__(self, rewrite=False):
        self._cmd = Command(
            "podman", "run", "-it", "-v", "/src/app:/app", "app"
        ).in_dir(PROJECT_DIRECTORY)
        self._rewrite = rewrite

    def set_up(self):
        self._iprocess = ICommand(self._cmd).run()

    def expect(self, text):
        self._iprocess.wait_until_output_contains(text)

    def display(self, expected_text):
        try:
            self._iprocess.wait_for_stripshot_to_match(
                expected_text,
                timeout=2,
            )
        except IProcessTimeout as error:
            if self._rewrite:
                self.current_step.rewrite("expected_text").to(error.stripshot)
            else:
                strings_match(expected_text, error.stripshot)

    def enter_text(self, text):
        self._iprocess.send_keys(f"{text}\n")

    def exit_successfully(self):
        self._iprocess.wait_for_successful_exit()

    def pause(self):
        import IPython

        IPython.embed()

    def tear_down(self):
        Command("podman", "stop", "app", "--time", "1", "-i").run()

    def on_failure(self, result):
        pass

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
