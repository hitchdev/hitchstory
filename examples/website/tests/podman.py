from commandlib import CommandError
from playwright.sync_api import sync_playwright


class App:
    """Run and interact with the web server."""

    def __init__(self, podman):
        self._podman = podman

    def start(self):
        self._podman(
            "run", "--rm", "-v", "/src/app:/app", "-d", "--name", "app", "app"
        ).output()

    def wait_until_ready(self):
        """Wait for port message"""
        logs = self._podman("logs", "-f", "app").interact().run()
        logs.wait_until_output_contains("Running on http://127.0.0.1:5000")
        logs.kill()

    def stop(self):
        self._podman("stop", "app", "--time", "1").ignore_errors().output()

    def logs(self):
        try:
            self._podman("logs", "app").run()
        except CommandError:
            pass


class PlaywrightServer:
    """
    Runs the server, grab a new page.
    """

    def __init__(self, podman, vnc=False):
        self._podman = podman
        self._ws = None
        self._vnc = vnc

    def start(self):
        cmd = [
            "run",
            "--rm",
            "-d",
        ]
        if self._vnc:
            cmd = cmd + [
                "-e",
                "PWDEBUG=console",
            ]
        cmd = cmd + ["--name", "playwright", "playwright"]
        self._podman(*cmd).output()

    def wait_until_ready(self):
        """Wait for logs to print out port."""
        logs = self._podman("logs", "-f", "playwright").interact().run()
        logs.wait_until_output_contains("Listening on")
        self._ws = logs.stripshot().replace("Listening on", "").strip()
        logs.kill()
        import time

        time.sleep(5)
        self._ws = "ws://127.0.0.1:3605"

    def stop(self):
        if hasattr(self, "_browser"):
            self._browser.close()
        if hasattr(self, "_playwright"):
            self._playwright.stop()
        try:
            self._podman("stop", "playwright", "--time", "1").ignore_errors().output()
        except CommandError:
            pass

    def new_page(self, browser_type="chromium"):
        self._playwright = sync_playwright().start()
        self._browser = getattr(self._playwright, browser_type).connect(self._ws)

        # .new_context(
        # record_video_dir="videos/"
        # )
        self._page = self._browser.new_page()
        self._page.set_default_navigation_timeout(10000)
        self._page.set_default_timeout(10000)
        return self._page
