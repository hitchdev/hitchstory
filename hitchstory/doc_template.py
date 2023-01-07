from strictyaml import Map, Str, load, MapPattern


class DocTemplate(object):
    def __init__(self, story_collection, doc_yaml_template, variables):
        self._story_collection = story_collection
        self._doc_yaml_template = doc_yaml_template
        self.variables = variables

    def parse(self):
        self._parsed = load(
            self._doc_yaml_template,
            Map(
                {
                    "story": Str(),
                    "given": MapPattern(Str(), Str()),
                    "steps": MapPattern(Str(), Str()),
                    "info": MapPattern(Str(), Str()),
                }
            ),
        ).data

    def validate(self):
        pass

    @property
    def story(self):
        return self._parsed["story"]

    @property
    def given(self):
        return self._parsed["given"]

    @property
    def steps(self):
        return self._parsed["steps"]

    @property
    def info(self):
        return self._parsed["info"]
