"""
Set up, run and interact with the application under test
using podman-compose.yml.

Potential improvements:

* More directed error handling (currently it dumps the output of all of the logs).
"""
from commandlib import python_bin, Command
from utils import port_open, wait_for_port
from db_fixtures import DbFixture
from hitchstory import Failure
from pathlib import Path
import hashlib
import socket
import json
import time


PROJECT_DIR = Path(__file__).absolute().parents[0].parent


class Services:
    """
    Sets up and runs the necessary services with podman-compose.
    """

    def __init__(self, env, ports=None, timeout=10.0):
        self._podman = Command("podman").in_dir(PROJECT_DIR)
        self._compose = python_bin.podman_compose.with_env(**env).in_dir(PROJECT_DIR)
        self._ports = ports
        self._timeout = timeout

    def start(self, db_fixture: DbFixture):
        """Start the services."""
        for port in self._ports:
            if port_open(port):
                raise Failure(f"Port {port} in use. Is another test running?")

        self._set_up_database(db_fixture)
        self._compose("up", "-d").output()
        self._wait_for_ports()

    def _set_up_database(self, db_fixture: DbFixture):
        db_fixture.build(self._compose)

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

    def _wait_for_ports(self):
        """Service readiness checker."""
        for port in self._ports:
            wait_for_port(port, timeout=self._timeout)

    def logs(self):
        self._compose("logs").run()

    def weblogs(self):
        self._compose("logs", "app").run()

    def stop(self):
        self._compose("down", "-t", "1").output()
