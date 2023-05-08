"""
This module contains the:

* Code that translates all of the YAML stories into pytest tests.
* Story Engine that interprets and validates the steps.
"""
from hitchstory import BaseEngine, InfoDefinition, InfoProperty, StoryCollection
from hitchstory import GivenDefinition, GivenProperty
from strictyaml import CommaSeparated, Enum, Str
from podman import PlaywrightServer, App
from playwright.sync_api import expect
from video import convert_to_slow_gif
from commandlib import Command, python_bin
from playwright.sync_api import sync_playwright
from slugify import slugify
from pathlib import Path
from os import getenv
import nest_asyncio
import sys

nest_asyncio.apply()

PROJECT_DIR = Path(__file__).absolute().parents[0].parent


class Engine(BaseEngine):
    """Python engine for interpreting and validating stories."""

    # Custom metadata about the stories
    # See docs: https://hitchdev.com/hitchstory/using/engine/metadata/
    info_definition = InfoDefinition(
        context=InfoProperty(schema=Str()),
        jiras=InfoProperty(schema=CommaSeparated(Str())),
    )

    # Preconditions
    # See docs: https://hitchdev.com/hitchstory/using/engine/given/
    given_definition = GivenDefinition(
        browser=GivenProperty(schema=Enum(["firefox", "chromium", "webkit"]))
    )

    def __init__(self, rewrite=False, vnc=False, timeout=10.0):
        """Initialize the engine"""
        self._rewrite = rewrite
        self._vnc = vnc
        self._timeout = int(timeout * 1000)
        self._compose = python_bin.podman_compose\
            .with_env(VNC="yes" if self._vnc else "no")\
            .in_dir(PROJECT_DIR)

    def set_up(self):
        """Run before running the tests."""
        self._compose("up", "-d").output()
        self._playwright = sync_playwright().start()
        self._browser = getattr(
            self._playwright, self.given["browser"]
        ).connect("ws://127.0.0.1:3605").new_context(
            record_video_dir="videos/",
            no_viewport=True,
        )
        self._page = self._browser.new_page()
        self._page.set_default_navigation_timeout(self._timeout)
        self._page.set_default_timeout(self._timeout)

    ## STEP METHODS
    def load_website(self):
        self._page.goto("http://localhost:5000")
        self._screenshot()

    def enter(self, on, text):
        self._page.get_by_test_id(slugify(on)).fill(text)

    def click(self, on):
        self._page.get_by_test_id(slugify(on)).click()

    def _screenshot(self):
        if self._rewrite:
            self._page.screenshot(
                path=PROJECT_DIR
                / "docs"
                / "{}-{}-{}.png".format(
                    self.story.slug,
                    self.current_step.index,
                    self.current_step.slug,
                )
            )

    def should_appear(self, on, text, which=None):
        if which is None:
            item = self._page.get_by_test_id(slugify(on))
        else:
            which = 0 if which == "first" else int(which) - 1
            item = self._page.locator(".test-{}".format(slugify(on))).nth(which)
        expect(item).to_contain_text(text)
        self._screenshot()

    def pause(self):
        """Special step that pauses a test."""
        if sys.stdout.isatty():
            __import__("IPython").embed()

    ## FINISHING UP
    def tear_down(self):
        """Tear down all test."""
        if hasattr(self, "_browser"):
            self._browser.close()
        if hasattr(self, "_playwright"):
            self._playwright.stop()
        self._compose("down", "-t", "1").output()

    def on_failure(self, result):
        """Run before teardown - save HTML, screenshot and video to docs."""
        if self._vnc:
            self.pause()
        if hasattr(self, "_page"):
            self._page.screenshot(path=PROJECT_DIR / "docs" / "failure.png")
            PROJECT_DIR.joinpath("docs", "failure.html").write_text(
                self._page.content()
            )
            self._page.close()
            self._page.video.save_as(PROJECT_DIR / "docs" / "failure.webm")
        if hasattr(self, "_compose"):
            self._compose("logs").run()

    def on_success(self):
        """Run before teardown, only on success."""
        if self._vnc:
            self.pause()

        self._page.close()

        if self._rewrite:
            self.new_story.save()
            webm_path = PROJECT_DIR / "docs" / f"{self.story.slug}.webm"
            self._page.video.save_as(webm_path)
            convert_to_slow_gif(webm_path)



collection = StoryCollection(
    # Grab all *.story YAML files in this directory
    Path(__file__).parent.parent.joinpath("story").glob("*.story"),
    Engine(
        rewrite=getenv("STORYMODE", "") == "rewrite",
        vnc=getenv("STORYMODE", "") == "vnc",
        timeout=10.0,
    ),
)

# Turn them into pytest tests
collection.with_external_test_runner().ordered_by_name().add_pytests_to(
    module=__import__(__name__)  # This module
)
