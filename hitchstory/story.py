from hitchstory.result import ResultList, Success, Failure
from hitchstory.story_step import StoryStep
from hitchstory import exceptions
from hitchstory import utils
from slugify import slugify
from path import Path
import prettystack
import time
import copy


THIS_DIRECTORY = Path(__file__).realpath().dirname()


DEFAULT_STACK_TRACE = prettystack.PrettyStackTemplate()\
                                 .to_console()\
                                 .cut_calling_code(
                                      THIS_DIRECTORY.joinpath("story_step.py")
                                 )


class Story(object):
    def __init__(
        self,
        story_file,
        name,
        parsed_yaml,
        engine,
        collection,
        parent=None,
        variation=False
    ):
        self._story_file = story_file
        self._name = name
        self._slug = None
        self._parsed_yaml = parsed_yaml
        self._engine = engine
        self._steps = []
        self._about = {}
        self._parent = parent
        if engine.schema.about is not None:
            for about_property in engine.schema.about.keys():
                self._about[about_property] = parsed_yaml.get(about_property)
        self._collection = collection
        self.variation = variation

    def update(self, step, kwargs):
        self._story_file.update(self, step, kwargs)

    @property
    def based_on(self):
        return str(self._parsed_yaml['based on']) \
            if "based on" in self._parsed_yaml else self._parent

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
    def child_name(self):
        return self._name

    @property
    def name(self):
        return self._name if not self.variation\
            else "{0}/{1}".format(self._parent, self._name)

    @property
    def slug(self):
        if self._slug is None:
            self._slug = slugify(self.name)
        return self._slug

    @property
    def based_on_story(self):
        return self._collection.without_filters().in_any_filename().named(self.based_on)

    @property
    def params(self):
        param_dict = self.based_on_story.params \
            if self.based_on is not None else {}
        for name, param in self._parsed_yaml.get("with", {}).items():
            param_dict[name] = param.data
        for name, param in self._collection._params.items():
            param_dict[name] = param
        return param_dict

    def unparameterized_preconditions(self):
        precondition_dict = self.based_on_story.unparameterized_preconditions() \
            if self.based_on is not None else {}
        for name, precondition in self._parsed_yaml.get("given", {}).items():
            precondition_dict[str(name)] = precondition.data
        return precondition_dict

    @property
    def preconditions(self):
        precondition_dict = self.unparameterized_preconditions()
        for name, precondition in precondition_dict.items():
            if utils.is_parameter(precondition):
                precondition_dict[name] = \
                    self.params[utils.parameter_name(precondition)]
            else:
                precondition_dict[name] = precondition
        return precondition_dict

    @property
    def parent_steps(self):
        return self.based_on_story.steps \
            if self.based_on is not None else []

    @property
    def steps(self):
        step_list = self.parent_steps
        step_list.extend(self._parsed_yaml.get('steps', []))
        return step_list

    @property
    def scenario(self):
        number_of_parent_steps = len(self.parent_steps)
        return [
            StoryStep(
                self, parsed_step, index, index - number_of_parent_steps, self.params
            ) for index, parsed_step in enumerate(self.steps)
        ]

    def run_special_method(self, method, exception_to_raise, result=None):
        try:
            if result is None:
                method()
            else:
                method(result)
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

            if current_step is not None and current_step.expect_exception(
                self._engine, caught_exception
            ):
                failure_stack_trace = DEFAULT_STACK_TRACE.only_the_exception().current_stacktrace()
            else:
                failure_stack_trace = DEFAULT_STACK_TRACE.current_stacktrace()

        if passed:
            self.run_special_method(self._engine.on_success, exceptions.OnSuccessException)
            result = Success(self, time.time() - start_time)
        else:
            result = Failure(
                self,
                time.time() - start_time,
                caught_exception,
                current_step,
                failure_stack_trace,
            )
            self.run_special_method(
                self._engine.on_failure,
                exceptions.OnFailureException,
                result=result
            )

        self.run_special_method(self._engine.tear_down, exceptions.TearDownException)
        return result


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
