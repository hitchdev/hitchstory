from hitchstory import BaseEngine, Failure, no_stacktrace_for, strings_match
from hitchstory import GivenDefinition, GivenProperty, InfoDefinition, InfoProperty
from strictyaml import Optional, Str, Map, Int, Bool, Enum, load, MapPattern
from icommandlib import ICommand, IProcessTimeout
from commandlib import Command
from path import Path


class Engine(BaseEngine):
    """Python engine for running tests."""

    def __init__(self, paths, rewrite=False):
        self._path = paths
        self._cmd = Command(
            "podman", "run", "-it", "-v", "/src/app:/app", "app"
        ).in_dir(self._path.project)
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
