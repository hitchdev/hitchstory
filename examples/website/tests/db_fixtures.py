"""
Code that manages the creation and loading of database fixtures.

Currently it loads data into a database using Django only, but with
some tweaking you could use it to create a JSON file which any
containerized database could load.

"""
from strictyaml import Enum, Int, Str, MapPattern, Bool, Map, Int
from pathlib import Path
import hashlib
import json

PROJECT_DIR = Path(__file__).absolute().parents[0].parent

FIXTURE_SCHEMA =  MapPattern(
    Enum(["todos.todo"]),
    MapPattern(
        Int(),
        Map(
            {
                "title": Str(),
                "created_at": Str(),
                "update_at": Str(),
                "isCompleted": Bool(),
            }
        ),
    ),
)

class DbFixture:
    def __init__(self, data):
        self._data = data
    
    @property
    def datahash(self):
        """Used to cache built fixtures as podman volumes."""
        return hashlib.md5(json.dumps(self._data, sort_keys=True).encode()).hexdigest()[:10]

    def build(self, compose):
        """Builds Django fixtures and runs the loaddata command."""
        fixture_data = []

        for model, model_data in self._data.items():
            for pk, fields in model_data.items():
                fixture_data.append(
                    {
                        "model": model,
                        "pk": pk,
                        "fields": fields,
                    }
                )

        Path(PROJECT_DIR).joinpath("app", "given.json").write_text(
                json.dumps(fixture_data, indent=4)
            )
        compose("run", "app", "migrate").output()
        compose("run", "app", "loaddata", "-i", "given.json").output()
        Path(PROJECT_DIR).joinpath("app", "given.json").unlink()
