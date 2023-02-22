from strictyaml import load, Map, Str, Seq, Optional, MapPattern, Any, YAMLError
from hitchstory import exceptions, utils
from hitchstory.story import Story
from path import Path
import copy


def _step_type(yaml_story):
    """Determine the step type of a story YAML snippet."""
    if "steps" in yaml_story:
        return "steps"
    elif "replacement_steps" in yaml_story:
        return "replacement_steps"
    elif "following_steps" in yaml_story:
        return "following_steps"
    else:
        raise NotImplementedError(
            "This should never happen - please raise "
            "a ticket on github.com/hitchdev/hitchstory"
        )


class StoryFile(object):
    """
    YAML file containing one or more named stories, part of a collection.
    """

    def __init__(self, filename, collection):
        self._filename = Path(filename).abspath()
        self._yaml = self._filename.bytes().decode("utf8")
        self._collection = collection
        self._updated_yaml = None

        steps_schema = Seq(Str() | MapPattern(Str(), Any(), maximum_keys=1))

        story_schema = {
            Optional("replacement_steps"): steps_schema,
            Optional("following_steps"): steps_schema,
            Optional("steps"): steps_schema,
            Optional("about"): Str(),
            Optional("with"): Any(),
            Optional("given"): self.engine.given_definition.preconditions,
        }

        # TODO : Make copy of story schema
        variation_schema = {
            Optional("replacement_steps"): steps_schema,
            Optional("following_steps"): steps_schema,
            Optional("steps"): steps_schema,
            Optional("about"): Str(),
            Optional("with"): Any(),
            Optional("given"): self.engine.given_definition.preconditions,
        }

        for info_property, info_property_schema in self.engine.info_definition.items():
            story_schema[Optional(info_property)] = info_property_schema
            variation_schema[Optional(info_property)] = info_property_schema

        story_schema[Optional("based_on")] = Str()
        story_schema[Optional("variations")] = MapPattern(
            Str(), Map(variation_schema, key_validator=utils.UnderscoredSlug())
        )

        try:
            self._parsed_yaml = load(
                self._yaml,
                Str()
                | MapPattern(
                    Str(), Map(story_schema, key_validator=utils.UnderscoredSlug())
                ),
            )
        except YAMLError as error:
            raise exceptions.StoryYAMLError(filename, str(error))

    @property
    def engine(self):
        return self._collection.engine

    def rewrite(self):
        """
        Rewrite all changes back to the file.
        """
        if self._updated_yaml is not None:
            self.path.write_text(self._updated_yaml.as_yaml())

    def update(self, story, step, kwargs):
        """
        Update a specific step in a particular story during a test run.
        """
        if self._updated_yaml is None:
            self._updated_yaml = copy.copy(self._parsed_yaml)

        if story.variation:
            if step.child_index >= 0:
                variations = self._updated_yaml[story.based_on]["variations"]
                yaml_story = variations[story.child_name]

                step_type = _step_type(yaml_story)

                if step.arguments.single_argument:
                    value = list(kwargs.values())[0]
                    yaml_story[step_type][step.child_index][step.name] = value
                else:
                    for key, value in kwargs.items():
                        yaml_story[step_type][step.child_index][step.name][key] = value
            else:
                yaml_story = self._updated_yaml[story.based_on]

                step_type = _step_type(yaml_story)

                if step.arguments.single_argument:
                    value = list(kwargs.values())[0]
                    yaml_story[step_type][step.index][step.name] = value
                else:
                    for key, value in kwargs.items():
                        yaml_story[step_type][step.index][step.name][key] = value
        else:
            yaml_story = self._updated_yaml[story.name]
            step_to_update = yaml_story[_step_type(yaml_story)][step.index]

            if step.arguments.single_argument:
                value = list(kwargs.values())[0]
                step_to_update[step.name] = value
            else:
                for key_to_update, value_to_update in kwargs.items():
                    step_to_update[step.name][key_to_update] = value_to_update

    @property
    def filename(self):
        return self._filename

    @property
    def collection(self):
        return self._collection

    @property
    def path(self):
        return Path(self._filename)

    def ordered_by_file(self):
        """
        Return all of the stories in the file in the order they
        appear in the file.
        """
        stories = []
        if self._parsed_yaml.is_mapping():
            for name, parsed_main_story in self._parsed_yaml.items():
                base_story = Story(self, str(name), parsed_main_story)
                stories.append(base_story)
                variations = []

                for variation_name, parsed_var_name in (
                    self._parsed_yaml[name].get("variations", {}).items()
                ):
                    variations.append(
                        Story(
                            self,
                            variation_name,
                            parsed_var_name,
                            variation_of=str(name),
                        )
                    )

                stories.extend(variations)
                base_story.variations = variations
        return stories
