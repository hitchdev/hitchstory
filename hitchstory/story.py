from path import Path
from strictyaml import load, Map, Str, Seq, MapPattern, Any, CommentedYAML
from hitchstory import utils
from ruamel.yaml.comments import CommentedMap
from hitchstory import exceptions
from hitchstory.arguments import Arguments
from hitchstory.result import Success, Failure
import time


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
    def __init__(self, yaml, name, engine):
        self._yaml = yaml
        self._engine = engine
        parsed_yaml = load(
            yaml,
            MapPattern(
                Str(),
                Map({
                    "scenario": Seq(CommentedYAML())
                })
            )
        )[name]
        self._name = name
        self._steps = []

        for index, parsed_step in enumerate(parsed_yaml['scenario']):
            self._steps.append(StoryStep(parsed_step, index))

    def play(self):
        try:
            self._engine.set_up()
            for step in self._steps:
                step.run(self._engine)
            self._engine.tear_down()
            result = Success(self)
        except Exception as exception:
            self._engine.tear_down()
            result = Failure(self, exception)
        return result


#class StoryFile(object):
    #def __init__(self, filename):
        #self._filename = filename

    #def story(self, engine):
        #return Story(Path(self._filename).bytes().decode('utf8'), engine)


class StoryCollection(object):
    def __init__(self, path, engine):
        assert isinstance(engine, BaseEngine)
        self._path = path
        self._engine = engine

    def story(self, filename, name):
        return Story(Path(self._path).joinpath(filename).bytes().decode('utf8'), name, self._engine)
