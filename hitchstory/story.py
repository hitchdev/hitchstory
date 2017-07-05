from strictyaml import load, Map, Str, Seq, Optional, MapPattern, Any, YAML
from hitchstory.result import ResultList, Success, Failure
from hitchstory.arguments import Arguments
from hitchstory import exceptions
from hitchstory import utils
from slugify import slugify
from path import Path
import prettystack
import strictyaml
import inspect
import time
import copy


THIS_DIRECTORY = Path(__file__).realpath().dirname()


DEFAULT_STACK_TRACE = prettystack.PrettyStackTemplate()\
                                 .to_console()\
                                 .cut_calling_code(
                                    THIS_DIRECTORY.joinpath("story.py"))\


class StoryStep(object):
    def __init__(self, story, yaml_step, index, params):
        self._yaml = yaml_step
        self._story = story
        self._index = index
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

    def update(self, **kwargs):
        self._story.update(self, kwargs)

    @property
    def index(self):
        return self._index

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
                        kwargs = {
                            key.data: val for key, val in \
                                self.arguments.kwargs.items()
                        }
                        step_method(**kwargs)
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

    def update(self, step, kwargs):
        self._story_file.update(self, step, kwargs)

    @property
    def story_file(self):
        return self._story_file

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
            precondition_dict[str(name)] = precondition
        return precondition_dict

    @property
    def preconditions(self):
        precondition_dict = self.unparameterized_preconditions()
        for name, precondition in precondition_dict.items():
            precondition_value = precondition.data \
                if isinstance(precondition, YAML) else precondition
            for param_name, param in self.params.items():
                precondition_value = utils.replace_parameter(precondition_value, param_name, param)
            precondition_dict[str(name)] = precondition_value
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
                self, parsed_step, index, self.params
            ) for index, parsed_step in enumerate(self.steps)
        ]

    def run_special_method(self, method, exception_to_raise):
        try:
            method()
        except Exception as exception:
            stack_trace = DEFAULT_STACK_TRACE.current_stacktrace()

            raise exception_to_raise(
                stack_trace
            )

    def play(self):
        """
        Run a story from beginning to end, time it and return
        a Result object.
        """
        start_time = time.time()
        passed = False
        caught_exception = None
        try:
            from signal import signal, SIGINT, SIGTERM, SIGHUP, SIGQUIT

            signal(SIGINT, self._engine.on_abort)
            signal(SIGTERM, self._engine.on_abort)
            signal(SIGHUP, self._engine.on_abort)
            signal(SIGQUIT, self._engine.on_abort)

            current_step = None
            self._engine._preconditions = self.preconditions
            self._engine.story = self
            self._engine.set_up()

            for step in self.scenario:
                current_step = step
                self._engine.current_step = current_step
                step.run(self._engine)
            passed = True
        except Exception as exception:
            caught_exception = exception
            failure_stack_trace = DEFAULT_STACK_TRACE.current_stacktrace()

        if passed:
            self.run_special_method(self._engine.on_success, exceptions.OnSuccessException)
            result = Success(self, time.time() - start_time)
        else:
            self.run_special_method(self._engine.on_failure, exceptions.OnFailureException)
            result = Failure(
                self,
                time.time() - start_time,
                caught_exception,
                current_step,
                failure_stack_trace
            )

        self.run_special_method(self._engine.tear_down, exceptions.TearDownException)
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

        if self._engine.schema.about is not None:
            for about_property, property_schema in self._engine.schema.about.items():
                story_schema[about_property] = property_schema

        story_schema['params'] = self._engine.schema.params
        story_schema['preconditions'] = self._engine.schema.preconditions

        # Load YAML into memory
        try:
            self._parsed_yaml = load(
                self._yaml,
                MapPattern(Str(), Map(story_schema))
            )
            self._updated_yaml = copy.copy(self._parsed_yaml)
        except strictyaml.YAMLError as error:
            raise exceptions.StoryYAMLError(
                filename, str(error)
            )

    def update(self, story, step, kwargs):
        """
        Update a specific step in a particular story during a test run.
        """
        if step.arguments.single_argument:
            self._updated_yaml[story.name]['scenario'][step.index][step.name] = \
                load(list(kwargs.values())[0])
        else:
            for key, value in kwargs.items():
                self._updated_yaml[story.name]['scenario'][step.index][step.name][key] = \
                    load(value)

    @property
    def filename(self):
        return self._filename

    @property
    def path(self):
        return Path(self._filename)

    def ordered_arbitrarily(self):
        """
        Return all of the stories in the file.
        """
        stories = []
        for name, self._parsed_yaml in self._parsed_yaml.items():
            stories.append(Story(self, str(name), self._parsed_yaml, self._engine, self._collection))
        return stories


class NewStory(object):
    def __init__(self, engine):
        self._engine = engine

    def save(self):
        """
        Write out the updated story to file.
        """
        story_file = self._engine.story.story_file
        story_file.path.write_text(
            story_file._updated_yaml.as_yaml()
        )


class StoryList(object):
    """
    A sequence of stories ready to be played in order.
    """

    def __init__(self, stories):
        for story in stories:
            assert type(story) is Story
        self._stories = stories
        self._continue_on_failure = False

    def continue_on_failure(self):
        new_story_list = copy.copy(self)
        new_story_list._continue_on_failure = True
        return new_story_list

    def play(self):
        results = ResultList()
        for story in self._stories:
            result = story.play()
            results.append(result)

            if not result.passed and not self._continue_on_failure:
                break
        return results

    def __len__(self):
        return len(self._stories)

    def __getitem__(self, index):
        return self._stories[index]
