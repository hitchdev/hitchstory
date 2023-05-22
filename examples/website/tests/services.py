"""
Set up, run and interact with the application under test
using podman-compose.yml.

Potential improvements:

* More directed error handling (currently it dumps the output of all of the logs).
"""
from commandlib import python_bin, Command
from commandlib.exceptions import CommandExitError
from utils import port_open
from db_fixtures import DbFixture
from hitchstory import Failure
from pathlib import Path
import json
import time


PROJECT_DIR = Path(__file__).absolute().parents[0].parent


class Services:
    """
    * Sets up and runs the necessary services with podman-compose.
    * Calls out to set up the db fixtures beforehand.
    * Waits for services to be ready before letting the rest of the test proceed.
    """

    def __init__(self, env, ports=None, timeout=10.0):
        self._podman = Command("podman").in_dir(PROJECT_DIR)
        self._compose = python_bin.podman_compose.with_env(**env).in_dir(PROJECT_DIR)
        self._ports = ports
        self._timeout = timeout

    def start(self, db_fixture: DbFixture):
        """Start the services."""
        for port in self._ports:
            if port_open(port, timeout=0.01):
                raise Failure(f"Port {port} in use. Is another test running?")

        self._set_up_database(db_fixture)
        self._compose("up", "--remove-orphans", "-d").output()
        self._healthcheck_all_services()
    
    
    def _healthcheck(self, container_id, times=3, interval=1.0):
        for _ in range(times):
            try:
                self._podman("healthcheck", "run", container_id).output()
                return True
            except CommandExitError:
                pass
            time.sleep(interval)
        return False
    
    def _healthcheck_all_services(self):
        for container_id in self._podman("ps", "-q").output().strip().split("\n"):
            if not self._healthcheck(container_id):
                raise Failure(
                    "Service '{}' failed:\n\n{}".format(
                        json.loads(self._podman("inspect", container_id).output())[0]["ImageName"],
                        self._podman("logs", container_id).output()
                    )
                )

    def _set_up_database(self, db_fixture: DbFixture):
        cachepath = Path("/gen/datacache-{}.tar".format(db_fixture.datahash))
        self._podman("volume", "rm", "src_db-data", "-f").output()

        if cachepath.exists():
            self._podman("volume", "create", "src_db-data").output()
            self._podman("volume", "import", "src_db-data", cachepath).output()
        else:
            db_fixture.build(self._compose)

            if cachepath.exists():
                cachepath.unlink()
            self._podman("volume", "export", "src_db-data", "-o", cachepath).run()

    def logs(self):
        self._compose("logs").run()

    def weblogs(self):
        self._compose("logs", "app").run()

    def stop(self):
        self._compose("down", "--remove-orphans", "-t", "1").output()
