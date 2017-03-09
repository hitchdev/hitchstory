from strictyaml import load, Map, Str, Seq, Optional, MapPattern, Any
from hitchstory.result import ResultList, Success, Failure
from hitchstory.arguments import Arguments
from hitchstory import exceptions
from hitchstory import utils
from slugify import slugify
from path import Path
import prettystack
import inspect
import time


THIS_DIRECTORY = Path(__file__).realpath().dirname()


class StoryStep(object):
    def __init__(self, yaml_step, index, params):
        self._yaml = yaml_step
        if isinstance(yaml_step.value, str):
            self.name = str(yaml_step)
            self.arguments = Arguments(None, params)
        elif isinstance(yaml_step.value, dict) and len(yaml_step.keys()) == 1:
            self.name = list(yaml_step.keys())[0]
            self.arguments = Arguments(list(yaml_step.values())[0], params)
        else:
            raise RuntimeError("Invalid YAML in step '{}'".format(yaml_step))

    def underscore_case_name(self):
        return utils.to_underscore_style(str(self.name))

    @property
    def yaml(self):
        return self._yaml

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
                    if type(self.arguments.argument) is str:
                        step_method(self.arguments.argument)
                    else:
                        step_method(self.arguments.argument.value)
                else:
                    argspec = inspect.getargspec(step_method)

                    if argspec.keywords is not None:
                        step_method(**self.arguments.kwargs.data)
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
        self._about = {}
        if engine.schema.about is not None:
            for about_property in engine.schema.about.keys():
                self._about[about_property] = parsed_yaml.get(about_property)
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
        param_dict = self._collection.named(str(self._parsed_yaml['based on'])).params \
            if "based on" in self._parsed_yaml else {}
        for name, param in self._parsed_yaml.get("params", {}).items():
            param_dict[name] = param
        return param_dict

    def unparameterized_preconditions(self):
        precondition_dict = {}
        precondition_dict = self._collection.named(
            str(self._parsed_yaml['based on'])
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
            precondition_dict[name] = precondition.data
        return precondition_dict

    @property
    def steps(self):
        step_list = self._collection.named(str(self._parsed_yaml['based on'])).steps \
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
            current_step = None
            self._engine._preconditions = self.preconditions
            self._engine.set_up()

            for step in self.scenario:
                current_step = step
                step.run(self._engine)

            self._engine.tear_down()
            result = Success(self, time.time() - start_time)
        except Exception as exception:
            self._engine.tear_down()
            stack_trace = prettystack.PrettyStackTemplate()\
                                     .cut_calling_code(
                                         THIS_DIRECTORY.joinpath("story.py"))\
                                     .to_console()\
                                     .current_stacktrace()
            result = Failure(
                self,
                time.time() - start_time,
                exception,
                current_step,
                stack_trace
            )
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
            Optional("scenario"): Seq(Any()),
            Optional("description"): Str(),
            Optional("based on"): Str(),
        }

        # Arrange YAML schema
        if self._engine.schema.params is not None:
            proposed_schema = {}
            for param, schema in self._engine.schema.params.items():
                proposed_schema[Optional(param)] = schema
            story_schema['params'] = Map(proposed_schema)

        if self._engine.schema.preconditions is not None:
            proposed_schema = {}
            for precondition, schema in self._engine.schema.preconditions.items():
                proposed_schema[Optional(precondition)] = schema
            story_schema['preconditions'] = Map(proposed_schema)

        if self._engine.schema.about is not None:
            for about_property, property_schema in self._engine.schema.about.items():
                story_schema[about_property] = property_schema

        # Load YAML into memory
        self._parsed_yaml = load(
            self._yaml,
            MapPattern(Str(), Map(story_schema))
        )

    @property
    def filename(self):
        return self._filename

    def ordered_arbitrarily(self):
        """
        Return all of the stories in the file.
        """
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
