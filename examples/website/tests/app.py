from commandlib import python_bin, Command
from pathlib import Path
import hashlib
import json


PROJECT_DIR = Path(__file__).absolute().parents[0].parent


class App:
    def __init__(self, env):
        self._podman = Command("podman").in_dir(PROJECT_DIR)
        self._compose = python_bin.podman_compose.with_env(**env).in_dir(PROJECT_DIR)
    
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

        datahash = hashlib.md5(json.dumps(data, sort_keys=True).encode()).hexdigest()[:10]
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
    
    def logs(self):
        self._compose("logs").run()
        
    def weblogs(self):
        self._compose("logs", "app").run()

    def stop(self):
        self._compose("down", "-t", "1").output()
