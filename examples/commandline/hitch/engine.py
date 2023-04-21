from hitchstory import BaseEngine, no_stacktrace_for
from hitchstory import GivenDefinition, GivenProperty, InfoDefinition, InfoProperty
from templex import Templex
from strictyaml import Optional, Str, Map, Int, Bool, Enum, load, MapPattern
from path import Path
from templex import Templex
from commandlib import Command
from icommandlib import ICommand
import requests
import time


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

    def display(self, text):
        time.sleep(0.5)
        try:
            Templex(text).assert_match(self._iprocess.stripshot())
        except AssertionError:
            if self._rewrite:
                self.current_step.update(text=self._iprocess.stripshot())
            else:
                raise

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
