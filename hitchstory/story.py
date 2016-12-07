from path import Path
from strictyaml import load, Map, Str, Seq, MapPattern, CommentedYAML
from hitchstory import utils
from ruamel.yaml.comments import CommentedMap
from hitchstory import exceptions
from hitchstory.arguments import Arguments
from hitchstory.result import ResultList, Success, Failure
from pathquery import pathq
import time
import copy


def validate(**kwargs):
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

    @property
    def preconditions(self):
        return self._preconditions

    def set_up(self):
        pass

    def tear_down(self):
        pass


class StoryStep(object):
    def __init__(self, yaml_step, index):
        if type(yaml_step) is str:
            self.name = str(yaml_step)
            self.arguments = Arguments(None)
        elif type(yaml_step) is CommentedMap and len(yaml_step.keys()) == 1:
            self.name = list(yaml_step.keys())[0]
            self.arguments = Arguments(list(yaml_step.values())[0])
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
    def __init__(self, story_file, name, parsed_yaml, engine):
        self._story_file = story_file
        self._name = name
        self._parsed_yaml = parsed_yaml
        self._engine = engine
        self._steps = []

    @property
    def filename(self):
        return self._story_file.filename

    @property
    def name(self):
        return self._name

    def play(self):
        start_time = time.time()
        try:
            self._engine._preconditions = self._parsed_yaml.get('preconditions')
            self._engine.set_up()
            for step in self._steps:
                step.run(self._engine)

            for index, parsed_step in enumerate(self._parsed_yaml['scenario']):
                step = StoryStep(parsed_step, index)
                self._steps.append(step)
                step.run(self._engine)

            self._engine.tear_down()
            result = Success(self, time.time() - start_time)
        except Exception as exception:
            self._engine.tear_down()
            result = Failure(self, time.time() - start_time, exception)
        return result


class StoryFile(object):
    def __init__(self, filename, engine):
        self._filename = filename
        self._yaml = filename.bytes().decode('utf8')
        self._engine = engine
        story_schema = {
            "scenario": Seq(CommentedYAML())
        }
        
        if self._engine.preconditions_schema is not None:
            story_schema['preconditions'] = engine.preconditions_schema

        self._parsed_yaml = load(
            self._yaml,
            MapPattern(Str(), Map(story_schema))
        )
        #self._steps = []
        #self._preconditions = parsed_yaml.get('preconditions')
    
    @property
    def filename(self):
        return self._filename

    def all(self):
        stories = []
        for name, parsed_yaml in self._parsed_yaml.items():
            stories.append(Story(self, name, parsed_yaml, self._engine))
        return stories


class StoryList(object):
    def __init__(self, stories):
        for story in stories:
            assert type(story) is Story
        self._stories = stories
    
    def play(self):
        results = ResultList()
        for story in self._stories:
            results.append(story.play())
        return results

    def __iter__(self):
        return self._stories


class StoryCollection(object):
    def __init__(self, path, engine):
        if not isinstance(engine, BaseEngine):
            raise exceptions.WrongEngineType(
                "Engine should inherit from hitchstory.BaseEngine."
            )
        self._path = path
        self._engine = engine
        self._filename = None

    def filename(self, name):
        new_collection = copy.copy(self)
        new_collection._filename = name
        return new_collection

    def all(self):
        if self._filename is None:
            stories = []
            for filename in pathq(self._path + "/*.story"):
                for story in StoryFile(filename, self._engine).all():
                    stories.append(story)
            return stories
    
    def ordered_by_name(self):
        stories = self.all()
        return StoryList(sorted(stories, key=lambda story: story.name))

    def one(self):
        stories = self.all()
        if len(stories) == 1:
            return stories[0]
        else:
            raise exceptions.MoreThanOneStory()

    #def story(self, filename, name):
        #return Story(Path(self._path).joinpath(filename), name, self._engine)
