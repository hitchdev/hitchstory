"""
Set up, run and interact with the application under test
using podman-compose.yml.

Potential improvements:

* Handle creation of database fixture creation / caching in a database agnostic way.
* More directed error handling (currently it dumps the output of all of the logs).
"""
from commandlib import python_bin, Command
from hitchstory import Failure
from pathlib import Path
import hashlib
import socket
import json
import time


PROJECT_DIR = Path(__file__).absolute().parents[0].parent


class App:
    def __init__(self, env, ports=None, timeout=10.0):
        self._podman = Command("podman").in_dir(PROJECT_DIR)
        self._compose = python_bin.podman_compose.with_env(**env).in_dir(PROJECT_DIR)
        self._ports = ports
        self._timeout = timeout

    def start(self, data=None):
        fixture_data = []

        for model, model_data in data.items():
            for pk, fields in model_data.items():
                fixture_data.append(
                    {
                        "model": model,
                        "pk": pk,
                        "fields": fields,
                    }
                )

        datahash = hashlib.md5(json.dumps(data, sort_keys=True).encode()).hexdigest()[
            :10
        ]
        cachepath = Path("/gen/datacache-{}.tar".format(datahash))
        self._podman("volume", "rm", "src_db-data", "-f").output()

        if cachepath.exists():
            self._podman("volume", "create", "src_db-data").output()
            self._podman("volume", "import", "src_db-data", cachepath).output()
        else:
            Path(PROJECT_DIR).joinpath("app", "given.json").write_text(
                json.dumps(fixture_data, indent=4)
            )
            self._compose("run", "app", "migrate").output()
            self._compose("run", "app", "loaddata", "-i", "given.json").output()
            Path(PROJECT_DIR).joinpath("app", "given.json").unlink()

            if cachepath.exists():
                cachepath.unlink()
            self._podman("volume", "export", "src_db-data", "-o", cachepath).run()
        self._compose("up", "-d").output()
        self._wait_for_ports()

    def _wait_for_ports(self):
        for port in self._ports:
            start_time = time.perf_counter()
            while True:
                try:
                    with socket.create_connection(
                        ("localhost", port), timeout=self._timeout
                    ):
                        break
                except OSError:
                    time.sleep(0.1)
                    if time.perf_counter() - start_time >= self._timeout:
                        raise Failure(
                            f"Port {port} on localhost not responding after {self._timeout} seconds."
                        )

    def logs(self):
        self._compose("logs").run()

    def weblogs(self):
        self._compose("logs", "app").run()

    def stop(self):
        self._compose("down", "-t", "1").output()
