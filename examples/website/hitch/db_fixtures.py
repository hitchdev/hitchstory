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
from commandlib import Command


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

    def __init__(self, data, compose):
        self._data = data
        self._podman = Command("podman").in_dir(DIR.PROJECT)
        self._compose = compose

    @property
    def datahash(self):
        """Unique hash identifying a fixture - used for caching."""
        return md5(
            bytes(self.VERSION) + dumps(self._data, sort_keys=True).encode()
        ).hexdigest()[:10]

    def build(self):
        """Builds Django fixtures and runs the loaddata command."""
        self._compose("up", "db", "-d").output()

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

        self._compose("run", "app", "migrate", "--noinput").output()
        self._compose(
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

        self._compose("run", "app", "loaddata", "-i", "given.json").output()
        given_json.unlink()

        self._compose("down", "db").output()

    def setup(self):
        cachepath = DIR.DATACACHE / "datacache-{}.tar".format(self.datahash)
        self._podman("volume", "rm", "hitch_db-data", "-f").output()

        if cachepath.exists():
            self._podman("volume", "create", "hitch_db-data").output()
            self._podman("volume", "import", "hitch_db-data", cachepath).output()
        else:
            self.build()

            if cachepath.exists():
                cachepath.unlink()
            self._podman("volume", "export", "hitch_db-data", "-o", cachepath).run()
