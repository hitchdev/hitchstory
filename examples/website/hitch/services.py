"""
Set up, run and interact with the application under test
using podman-compose.yml.

Potential improvements:

* More directed error handling (currently it dumps the output of all of the logs).
"""
from commandlib import python_bin, Command
from commandlib.exceptions import CommandExitError
from utils import port_open
from hitchstory import Failure
from pathlib import Path
from directories import DIR
from copy import copy
import json
import time


class Services:
    """
    * Sets up and runs the necessary services with podman-compose.
    * Waits for services to be healthy before proceeding.
    * Prints logs for the various services.
    """

    def __init__(self, env, ports=None, timeout=10.0):
        self._podman = Command("podman").in_dir(DIR.PROJECT)
        self._compose = (
            Command("podman-compose", "-f", "hitch/podman-compose.yml")
            .with_env(**env)
            .in_dir(DIR.PROJECT)
        )
        self._ports = ports
        self._timeout = timeout

    def start(self):
        """Start the services."""
        for port in self._ports:
            if port_open(port, timeout=0.01):
                raise Failure(f"Port {port} in use. Is another test running?")

        self._compose("up", "--remove-orphans", "-d").output()
        self._healthcheck_all_services()

    def _healthcheck_all_services(self, interval=0.2, retries=10):
        """
        Run healthchecks on all services and fail if any of them don't come up.

        This ought to really be done automatically by podman-compose, but
        it seems to lack the functionality right now:

        https://github.com/containers/podman-compose/discussions/697
        """
        container_ids = self._podman("ps", "-q").output().strip().split("\n")
        healthy_containers = []

        for _ in range(retries):
            for container_id in container_ids:
                if container_id not in healthy_containers:
                    try:
                        self._podman("healthcheck", "run", container_id).output()
                        healthy_containers.append(container_id)
                    except CommandExitError:
                        pass

            if len(healthy_containers) == len(container_ids):
                return

            time.sleep(interval)

        for container_id in container_ids:
            if container_id not in healthy_containers:
                raise Failure(
                    "Service '{}' failed:\n\n{}".format(
                        json.loads(self._podman("inspect", container_id).output())[0][
                            "ImageName"
                        ],
                        self._podman("logs", container_id).output(),
                    )
                )

    def logs(self):
        self._compose("logs").run()

    def weblogs(self):
        self._compose("logs", "app").run()

    def stop(self):
        self._compose("down", "--remove-orphans", "-t", "1").output()
