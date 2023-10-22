import time


class App:
    """Interact directly with the app via podman."""

    def __init__(self, podman):
        self._podman = podman

    def start(self):
        self._podman("run", "-v", "/src/app:/app", "-d", "app").output()

    def wait_until_ready(self):
        # Really bad way to do it
        time.sleep(1)

    def stop(self):
        self._podman("stop", "--latest", "--time", "1").output()

    def logs(self):
        self._podman("logs", "--latest").run()
