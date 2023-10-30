"""
Code that manages the creation and loading of database fixtures.

Currently it loads data into a database using Django only, but with
some tweaking you could use it to create a JSON file which any
containerized database could load.

"""
from strictyaml import Enum, Int, Str, MapPattern, Bool, Map, Int
from hashlib import md5
from json import dumps
from directories import DIR


FIXTURE_SCHEMA = MapPattern(
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
    VERSION = 2

    def __init__(self, data):
        self._data = data

    @property
    def datahash(self):
        """Unique hash identifying a fixture - used for caching."""
        return md5(
            bytes(self.VERSION) + dumps(self._data, sort_keys=True).encode()
        ).hexdigest()[:10]

    def build(self, compose):
        """Builds Django fixtures and runs the loaddata command."""
        compose("up", "db", "-d").output()

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

        given_json = DIR.APP / "given.json"
        given_json.write_text(dumps(fixture_data, indent=4))

        compose("run", "app", "migrate", "--noinput").output()
        compose(
            "run",
            "-e",
            "DJANGO_SUPERUSER_USERNAME=admin",
            "-e",
            "DJANGO_SUPERUSER_PASSWORD=password",
            "-e",
            "DJANGO_SUPERUSER_EMAIL=admin@admin.com",
            "app",
            "createsuperuser",
            "--noinput",
        ).output()

        compose("run", "app", "loaddata", "-i", "given.json").output()
        given_json.unlink()

        compose("down", "db").output()
