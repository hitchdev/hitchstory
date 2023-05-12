"""
This module contains the:

* Code that translates all of the YAML stories into pytest tests.
* Story Engine that interprets and validates the steps.
"""
from hitchstory import BaseEngine, InfoDefinition, InfoProperty, StoryCollection
from hitchstory import GivenDefinition, GivenProperty
from strictyaml import CommaSeparated, Enum, Int, Str, MapPattern, Bool, Map, Int
from hitchstory import no_stacktrace_for, validate
from playwright.sync_api import expect
from video import convert_to_slow_gif
from commandlib import Command, python_bin
from playwright.sync_api import sync_playwright
from compare_screenshots import compare_screenshots
from db_fixtures import FIXTURE_SCHEMA, DbFixture
from slugify import slugify
from pathlib import Path
from os import getenv
from app import Services
import nest_asyncio
import time
import sys

nest_asyncio.apply()

PROJECT_DIR = Path(__file__).absolute().parents[0].parent


class Engine(BaseEngine):
    """
    Python engine for validating, running and debugging YAML stories.
    """

    # Custom metadata about the stories
    # See docs: https://hitchdev.com/hitchstory/using/engine/metadata/
    info_definition = InfoDefinition(
        context=InfoProperty(schema=Str()),
        jiras=InfoProperty(schema=CommaSeparated(Str())),
        docs=InfoProperty(schema=Bool()),
    )

    # Preconditions
    # See docs: https://hitchdev.com/hitchstory/using/engine/given/
    given_definition = GivenDefinition(
        browser=GivenProperty(schema=Enum(["firefox", "chromium", "webkit"])),
        data=GivenProperty(
            schema=FIXTURE_SCHEMA,
            inherit_via=GivenProperty.OVERRIDE,
        ),
    )

    def __init__(self, rewrite=False, vnc=False, timeout=10.0):
        """Initialize the engine"""
        self._rewrite = rewrite
        self._vnc = vnc
        self._timeout = timeout
        self._services = Services(
            env={
                "VNC": "yes" if self._vnc else "no",
                "VNCSCREENSIZE": "1024x768",
            },
            ports=[3605, 8000],
            timeout=timeout,
        )

    def set_up(self):
        """Run before running the tests."""
        self._services.start(
            DbFixture(self.given.get("data", {})),
        )
        self._playwright = sync_playwright().start()
        self._browser = (
            getattr(self._playwright, self.given["browser"])
            .connect("ws://127.0.0.1:3605")
            .new_context(
                record_video_dir="videos/",
                no_viewport=True,
            )
        )
        self._page = self._browser.new_page()
        self._page.set_default_navigation_timeout(int(self._timeout * 1000))
        self._page.set_default_timeout(int(self._timeout * 1000))

    ## STEP METHODS
    def load_website(self, url):
        self._page.goto(f"http://localhost:8000/{url}")
        self._screenshot()

    def enter(self, on, text):
        self._page.get_by_test_id(slugify(on)).fill(text)

    def click(self, on):
        self._page.get_by_test_id(slugify(on)).click()

    @validate(which=Int())
    @no_stacktrace_for(AssertionError)
    def should_appear(self, on, text, which=None):
        try:
            expect(self._locate(on, which)).to_contain_text(text)
        except AssertionError:
            if self._rewrite:
                self._locate(on, which).click()  # does it even exist?
                self.current_step.rewrite("text").to(
                    self._locate(on, which).text_content().strip()
                )
            else:
                raise

        self._screenshot()

    def pause(self):
        """Special step that pauses a test and launches a REPL."""
        if sys.stdout.isatty():
            __import__("IPython").embed()

    ## HELPER METHODS
    def _locate(self, on, which):
        """
        Use high level information to pick locators.

        If it is one from a list (i.e. which) -> use CSS selector .test-SLUGIFIED
        If it is a single item -> use test ID with SLUGIFIED
        """
        if which is None:
            item = self._page.get_by_test_id(slugify(on))
        else:
            item = self._page.locator(".test-{}".format(slugify(on))).nth(which)
        return item

    def _screenshot(self):
        """
        Save screenshots associated with step for use in docs and
        compare them.
        """
        golden_snapshot = (
            PROJECT_DIR
            / "docs"
            / "{}-{}-{}.png".format(
                self.story.slug,
                self.current_step.index,
                self.current_step.slug,
            )
        )

        time.sleep(1)

        if self._rewrite:
            self._page.screenshot(path=golden_snapshot)
        else:
            if not self._vnc:
                compare_screenshots(
                    self._page.screenshot(),
                    golden_snapshot,
                    diff_snapshot_path=PROJECT_DIR / "artefacts" / "diff.png",
                    threshold=0.1,
                )

    ## FINISHING UP
    def tear_down(self):
        """Tear down all test."""
        if hasattr(self, "_browser"):
            self._browser.close()
        if hasattr(self, "_playwright"):
            self._playwright.stop()
        self._services.stop()

    def on_failure(self, result):
        """Run before teardown - save HTML, screenshot and video to docs on failure."""
        if self._vnc:
            print(result.stacktrace)
            self.pause()
        if hasattr(self, "_page"):
            self._page.screenshot(path=PROJECT_DIR / "artefacts" / "failure.png")
            PROJECT_DIR.joinpath("artefacts", "failure.html").write_text(
                self._page.content()
            )
            self._page.close()
            self._page.video.save_as(PROJECT_DIR / "artefacts" / "failure.webm")
        if hasattr(self, "_services"):
            self._services.logs()

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
collection.with_external_test_runner().only_uninherited().ordered_by_name().add_pytests_to(
    module=__import__(__name__)  # This module
)
