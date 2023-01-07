from strictyaml import Map, Str, load, MapPattern
from hitchstory.utils import to_underscore_style
import jinja2


class DocTemplate(object):
    def __init__(self, engine, doc_yaml_template, extra):
        self._doc_yaml_template = doc_yaml_template
        self.jenv = jinja2.Environment(
            undefined=jinja2.StrictUndefined, loader=jinja2.BaseLoader
        )
        self.jenv.globals.update(extra)
        self._engine = engine

    def parse(self):
        self._parsed = load(
            self._doc_yaml_template,
            Map(
                {
                    "story": Str(),
                    "given": Map(
                        {name: Str() for name in self._engine.given_definition.keys()}
                    ),
                    "steps": MapPattern(Str(), Str()),
                    "info": Map(
                        {name: Str() for name in self._engine.info_definition.keys()}
                    ),
                }
            ),
        ).data

        self._slugified_steps = {
            to_underscore_style(name): text
            for name, text in self._parsed["steps"].items()
        }

    def validate(self):
        pass

    def story(self):
        return self.jenv.from_string(self._parsed["story"])

    def given_from_name(self, name):
        return self.jenv.from_string(self._parsed["given"][name])

    def info_from_name(self, name):
        return self.jenv.from_string(self._parsed["info"][name])

    def step_from_slug(self, slug):
        return self.jenv.from_string(self._slugified_steps[slug])
