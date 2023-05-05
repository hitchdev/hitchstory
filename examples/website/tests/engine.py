from hitchstory import StoryCollection, BaseEngine
from hitchstory import exceptions, validate
from hitchstory import GivenDefinition, GivenProperty, InfoDefinition, InfoProperty
from strictyaml import Optional, Str, Map, Int, Bool, Enum, load, MapPattern
from playwright.sync_api import expect
from commandlib import Command, CommandError
from podman import PlaywrightServer, App
from video import convert_to_slow_gif
from slugify import slugify
from pathlib import Path
import nest_asyncio

nest_asyncio.apply()

PROJECT_DIR = Path(__file__).absolute().parents[0].parent


class Engine(BaseEngine):
    """Python engine for running tests."""

    info_definition = InfoDefinition(
        context=InfoProperty(schema=Str()),
    )

    def __init__(self, rewrite=False):
        self._rewrite = rewrite
        self._podman = Command("podman").in_dir(PROJECT_DIR)
        self._app = App(self._podman)
        self._playwright_server = PlaywrightServer(self._podman)

    def set_up(self):
        """Set up all tests."""
        self._podman("container", "rm", "--all").output()
        self._app.start()
        self._playwright_server.start()
        self._app.wait_until_ready()
        self._playwright_server.wait_until_ready()
        self._page = self._playwright_server.new_page()

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
        __import__("IPython").embed()

    def tear_down(self):
        """Tear down all tests"""
        if hasattr(self, "_playwright_server"):
            self._playwright_server.stop()
        if hasattr(self, "_app"):
            self._app.stop()

    def on_failure(self, result):
        """Run before teardown, only on failure."""
        if hasattr(self, "_page"):
            self._page.screenshot(path=PROJECT_DIR / "docs" / "failure.png")
            PROJECT_DIR.joinpath("docs", "failure.html").write_text(
                self._page.content()
            )
            self._page.close()
            self._page.video.save_as(PROJECT_DIR / "docs" / "failure.webm")
        if hasattr(self, "_app"):
            self._app.logs()

    def on_success(self):
        """Run before teardown, only on success."""
        self._page.close()

        if self._rewrite:
            self.new_story.save()
            webm_path = PROJECT_DIR / "docs" / f"{self.story.slug}.webm"
            self._page.video.save_as(webm_path)
            convert_to_slow_gif(webm_path)
