from strictyaml import load, Map, Str, Seq, Optional, MapPattern, CommentedYAML
from hitchstory import utils
from ruamel.yaml.comments import CommentedMap
from hitchstory import exceptions
from hitchstory.arguments import Arguments
from hitchstory.result import ResultList, Success, Failure
from path import Path
from slugify import slugify
import time
import copy


def validate(**kwargs):
    """
    Decorator for validating a HitchStory step.
    """
    def decorator(step_function):
        for arg in kwargs:
            if arg not in step_function.__code__.co_varnames:
                raise exceptions.StepContainsInvalidValidator(
                    "Step {} does not contain argument '{}' listed as a validator.".format(
                        step_function.__repr__(), arg
                    )
                )
        step_function._validators = kwargs
        return step_function
    return decorator


class BaseEngine(object):
    preconditions_schema = None
    about_schema = None
    params_schema = None

    @property
    def preconditions(self):
        return self._preconditions

    def set_up(self):
        pass

    def tear_down(self):
        pass


class StoryStep(object):
    def __init__(self, yaml_step, index, params):
        if type(yaml_step) is str:
            self.name = str(yaml_step)
            self.arguments = Arguments(None, params)
        elif type(yaml_step) is CommentedMap and len(yaml_step.keys()) == 1:
            self.name = list(yaml_step.keys())[0]
            self.arguments = Arguments(list(yaml_step.values())[0], params)
        else:
            raise RuntimeError("Invalid YAML in step '{}'".format(yaml_step))

    def underscore_case_name(self):
        return utils.to_underscore_style(self.name)

    def run(self, engine):
        if hasattr(engine, self.underscore_case_name()):
            attr = getattr(engine, self.underscore_case_name())
            if hasattr(attr, '__call__'):
                step_method = attr

                validators = step_method._validators \
                    if hasattr(step_method, '_validators') else {}
                self.arguments.validate(validators)

                if self.arguments.is_none:
                    step_method()
                elif self.arguments.single_argument:
                    step_method(self.arguments.argument)
                else:
                    step_method(**self.arguments.pythonized_kwargs())
            else:
                raise exceptions.StepNotCallable((
                    "Step with name '{}' in {} is not a function "
                    "or a callable object, it is a {}".format(
                        self.underscore_case_name(),
                        engine.__repr__(),
                        type(attr)
                    )
                ))
        else:
            raise exceptions.StepNotFound("Step with name '{}' not found in {}.".format(
                self.underscore_case_name(),
                engine.__repr__()
            ))


class Story(object):
    def __init__(self, story_file, name, parsed_yaml, engine, collection):
        self._story_file = story_file
        self._name = name
        self._parsed_yaml = parsed_yaml
        self._engine = engine
        self._steps = []
        self._about = parsed_yaml.get('about')
        self._collection = collection

    @property
    def filename(self):
        return self._story_file.filename

    @property
    def about(self):
        return self._about

    @property
    def name(self):
        return self._name

    @property
    def slug(self):
        return slugify(self._name)

    @property
    def params(self):
        param_dict = self._collection.named(self._parsed_yaml['based on']).params \
            if "based on" in self._parsed_yaml else {}
        for name, param in self._parsed_yaml.get("params", {}).items():
            param_dict[name] = param
        return param_dict

    def unparameterized_preconditions(self):
        precondition_dict = {}
        precondition_dict = self._collection.named(
            self._parsed_yaml['based on']
        ).unparameterized_preconditions() \
            if "based on" in self._parsed_yaml else {}
        for name, precondition in self._parsed_yaml.get("preconditions", {}).items():
            precondition_dict[name] = precondition
        return precondition_dict

    @property
    def preconditions(self):
        precondition_dict = self.unparameterized_preconditions()
        for name, precondition in precondition_dict.items():
            for param_name, param in self.params.items():
                precondition = utils.replace_parameter(precondition, param_name, param)
            precondition_dict[name] = precondition
        return precondition_dict

    @property
    def steps(self):
        step_list = self._collection.named(self._parsed_yaml['based on']).steps \
            if "based on" in self._parsed_yaml else []
        step_list.extend(self._parsed_yaml.get('scenario', []))
        return step_list

    @property
    def scenario(self):
        return [
            StoryStep(
                parsed_step, index, self.params
            ) for index, parsed_step in enumerate(self.steps)
        ]

    def play(self):
        start_time = time.time()
        try:
            self._engine._preconditions = self.preconditions
            self._engine.set_up()

            for step in self.scenario:
                step.run(self._engine)

            self._engine.tear_down()
            result = Success(self, time.time() - start_time)
        except Exception as exception:
            self._engine.tear_down()
            result = Failure(self, time.time() - start_time, exception)
        return result


class StoryFile(object):
    """
    YAML file containing one or more named stories, part of a collection.
    """
    def __init__(self, filename, engine, collection):
        self._filename = filename
        self._yaml = filename.bytes().decode('utf8')
        self._engine = engine
        self._collection = collection
        story_schema = {
            Optional("scenario"): Seq(CommentedYAML()),
            Optional("description"): Str(),
            Optional("based on"): Str(),
        }

        if self._engine.params_schema is not None:
            proposed_schema = {}
            for param, schema in self._engine.params_schema.items():
                proposed_schema[Optional(param)] = schema
            story_schema['params'] = Map(proposed_schema)

        if self._engine.preconditions_schema is not None:
            proposed_schema = {}
            for precondition, schema in self._engine.preconditions_schema.items():
                proposed_schema[Optional(precondition)] = schema
            story_schema['preconditions'] = Map(proposed_schema)

        if self._engine.about_schema is not None:
            story_schema['about'] = engine.about_schema

        self._parsed_yaml = load(
            self._yaml,
            MapPattern(Str(), Map(story_schema))
        )

    @property
    def filename(self):
        return self._filename

    def ordered_arbitrarily(self):
        stories = []
        for name, self._parsed_yaml in self._parsed_yaml.items():
            stories.append(Story(self, name, self._parsed_yaml, self._engine, self._collection))
        return stories


class StoryList(object):
    """
    A sequence of stories ready to be played in order.
    """

    def __init__(self, stories):
        for story in stories:
            assert type(story) is Story
        self._stories = stories

    def play(self):
        results = ResultList()
        for story in self._stories:
            results.append(story.play())
        return results

    def __len__(self):
        return len(self._stories)

    def __getitem__(self, index):
        return self._stories[index]


class StoryCollection(object):
    """
    Unordered group of related stories.
    """

    def __init__(self, storypaths, engine):
        if not isinstance(engine, BaseEngine):
            raise exceptions.WrongEngineType(
                "Engine should inherit from hitchstory.BaseEngine."
            )
        self._storypaths = storypaths
        self._engine = engine
        self._in_filename = None
        self._named = None
        self._filters = []

        self._stories = {}

        for filename in self._storypaths:
            for story in StoryFile(filename, self._engine, self).ordered_arbitrarily():
                if slugify(story.name) in self._stories:
                    raise exceptions.DuplicateStoryNames(story, self._stories[slugify(story.name)])
                self._stories[slugify(story.name)] = story

    def ordered_arbitrarily(self):
        """
        Return a StoryList object containing stories filtered
        from the collection.
        """
        stories = []
        for story in self._stories.values():
            filtered = True
            for filter_func in self._filters:
                if not filter_func(story):
                    filtered = False
            if self._named is not None:
                if story.name != self._named:
                    filtered = False
            if self._in_filename is not None:
                if Path(story.filename).abspath() != Path(self._in_filename).abspath():
                    filtered = False
            if filtered:
                stories.append(story)
        return stories

    def filter(self, filter_func):
        assert callable(filter_func)
        new_collection = copy.copy(self)
        new_collection._filters.append(filter_func)
        return new_collection

    def in_filename(self, filename):
        assert type(filename) is str
        new_collection = copy.copy(self)
        new_collection._in_filename = Path(filename)
        assert new_collection._in_filename.exists()
        return new_collection

    def named(self, name):
        """
        Return a single story object with the name specified.

        Only slugified names are compared. E.g. "Story NAME" and "story-name" are equivalent.
        """
        for story in self.ordered_arbitrarily():
            if slugify(name) == story.slug:
                return story
        raise exceptions.StoryNotFound(name)

    def ordered_by_name(self):
        """
        Return a list of stories ordered by name.
        """
        return StoryList(sorted(self.ordered_arbitrarily(), key=lambda story: story.name))

    def shortcut(self, *words):
        """
        Return a single story that matches all of the words.
        """
        matching = []
        for story in self.ordered_arbitrarily():
            if len([word for word in words if slugify(word) in story.slug]) == len(words):
                matching.append(story)
        if len(matching) == 0:
            raise exceptions.StoryNotFound(", ".join(words))
        elif len(matching) > 1:
            raise exceptions.MoreThanOneStory(
                "\n".join([
                    "{0} (in {1})".format(story.name, story.filename) for story in matching
                ])
            )
        else:
            return matching[0]

    def one(self):
        stories = self.ordered_arbitrarily()
        if len(stories) > 1:
            raise exceptions.MoreThanOneStory()
        elif len(stories) == 0:
            raise exceptions.NoStories()
        else:
            return stories[0]
