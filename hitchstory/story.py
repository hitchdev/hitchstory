from hitchstory.result import Success, Failure
from hitchstory.story_step import StoryStep
from hitchstory.utils import DEFAULT_STACK_TRACE
from hitchstory import exceptions
from hitchstory import utils
from slugify import slugify
import time


class Story(object):
    def __init__(self, story_file, name, parsed_yaml, parent=None, variation=False):
        self._story_file = story_file
        self._name = name
        self._slug = None
        self._parsed_yaml = parsed_yaml
        self._steps = []
        self._about = {}
        self._parent = parent
        if self.engine.schema.about is not None:
            for about_property in self.engine.schema.about.keys():
                self._about[about_property] = self.data.get(about_property)
        self._collection = self._story_file.collection
        self.variation = variation

    def update(self, step, kwargs):
        self._story_file.update(self, step, kwargs)

    @property
    def data(self):
        return self._parsed_yaml.data

    @property
    def based_on(self):
        return self.data['based on'] if "based on" in self.data else self._parent

    @property
    def story_file(self):
        return self._story_file

    @property
    def engine(self):
        return self._story_file.engine

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
        for name, param in self.data.get("with", {}).items():
            param_dict[name] = param
        for name, param in self._collection._params.items():
            param_dict[name] = param
        return param_dict

    def unparameterized_preconditions(self):
        precondition_dict = self.based_on_story.unparameterized_preconditions() \
            if self.based_on is not None else {}
        for name, precondition in self.data.get("given", {}).items():
            precondition_dict[name] = precondition
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
    def _parent_steps(self):
        return self.based_on_story._yaml_steps \
            if self.based_on is not None else []

    @property
    def _yaml_steps(self):
        step_list = self._parent_steps
        step_list.extend(self._parsed_yaml.get('steps', []))
        return step_list

    @property
    def steps(self):
        number_of_parent_steps = len(self._parent_steps)
        return [
            StoryStep(
                self, parsed_step, index, index - number_of_parent_steps, self.params
            ) for index, parsed_step in enumerate(self._yaml_steps)
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

    def run_on_success(self):
        try:
            self.engine.on_success()
        except Exception as exception:
            self.run_special_method(self.engine.tear_down, exceptions.TearDownException)
            stack_trace = DEFAULT_STACK_TRACE.current_stacktrace()

            raise exceptions.OnSuccessException(stack_trace)

    def run_on_failure(self, result):
        try:
            self.engine.on_failure(result)
        except Exception as exception:
            self.run_special_method(self.engine.tear_down, exceptions.TearDownException)
            stack_trace = DEFAULT_STACK_TRACE.current_stacktrace()

            raise exceptions.OnFailureException(stack_trace)

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

            signal(SIGINT, self.engine.on_abort)
            signal(SIGTERM, self.engine.on_abort)
            signal(SIGHUP, self.engine.on_abort)
            signal(SIGQUIT, self.engine.on_abort)

            current_step = None
            self.engine._preconditions = self.preconditions
            self.engine.story = self
            self.engine.set_up()

            for step in self.steps:
                current_step = step
                self.engine.current_step = current_step
                step.run()
            passed = True
        except Exception as exception:
            caught_exception = exception

            if current_step is not None and current_step.expect_exception(
                self.engine, caught_exception
            ):
                failure_stack_trace = DEFAULT_STACK_TRACE.only_the_exception().current_stacktrace()
            else:
                failure_stack_trace = DEFAULT_STACK_TRACE.current_stacktrace()

        if passed:
            self.run_on_success()
            result = Success(self, time.time() - start_time)
        else:
            result = Failure(
                self,
                time.time() - start_time,
                caught_exception,
                current_step,
                failure_stack_trace,
            )
            self.run_on_failure(result)

        self.run_special_method(self.engine.tear_down, exceptions.TearDownException)
        return result

    def __repr__(self):
        return u"Story('{0}')".format(self._slug)
