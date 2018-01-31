from hitchstory.result import Success, Failure
from hitchstory.story_step import StoryStep
from hitchstory.utils import DEFAULT_STACK_TRACE
from hitchstory import exceptions
from hitchstory import utils
from slugify import slugify
import colorama
import time


class StoryInfo():
    pass


class Story(object):
    def __init__(self, story_file, name, parsed_yaml, variation_of=None):
        self._story_file = story_file
        self._name = name
        self._slug = None
        self._parsed_yaml = parsed_yaml
        self._steps = []
        self._info = StoryInfo()
        self._parent = None
        self._variation_of = variation_of
        for info_property in self.engine.info_definition.keys():
            if info_property in self.data.keys():
                setattr(
                    self._info,
                    utils.underscore_slugify(info_property),
                    self.data.get(info_property),
                )
        self._collection = self._story_file.collection
        self.children = []

    def _unparameterized_preconditions(self):
        precondition_dict = self.parent._unparameterized_preconditions() \
            if self.parent is not None else {}
        for name, precondition in self.data.get("given", {}).items():
            precondition_dict[name] = precondition
        return precondition_dict

    @property
    def _yaml_steps(self):
        step_list = self._parent_steps
        step_list.extend(self._parsed_yaml.get('steps', []))
        return step_list

    @property
    def _parent_steps(self):
        return self.parent._yaml_steps \
            if self.parent is not None else []

    def _initialize(self):
        precondition_dict = self._unparameterized_preconditions()
        for name, precondition in precondition_dict.items():
            if utils.is_parameter(precondition):
                precondition_dict[name] = \
                    self.params[utils.parameter_name(precondition)]
            else:
                precondition_dict[name] = precondition
        self._precondition_dict = precondition_dict

        from strictyaml.compound import MapValidator, SeqValidator

        for name, definition in self.engine.given_definition.given_properties.items():
            if name not in self._precondition_dict.keys():
                if isinstance(definition.schema, MapValidator):
                    self._precondition_dict[name] = {}
                elif isinstance(definition.schema, SeqValidator):
                    self._precondition_dict[name] = []
                else:
                    self._precondition_dict[name] = None

        number_of_parent_steps = len(self._parent_steps)
        self._steps = [
            StoryStep(
                self, parsed_step, index, index - number_of_parent_steps, self.params
            ) for index, parsed_step in enumerate(self._yaml_steps)
        ]

    def update(self, step, kwargs):
        self._story_file.update(self, step, kwargs)

    @property
    def variation(self):
        return self._variation_of is not None

    @property
    def data(self):
        return self._parsed_yaml.data

    @property
    def based_on(self):
        return self.data['based on'] if "based on" in self.data else self._variation_of

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
    def info(self):
        return self._info

    @property
    def child_name(self):
        return self._name

    @property
    def name(self):
        return self._name if not self.variation\
            else "{0}/{1}".format(self._variation_of, self._name)

    @property
    def slug(self):
        if self._slug is None:
            self._slug = slugify(self.name)  # relatively slow method
        return self._slug

    @property
    def parent(self):
        return self._parent

    @property
    def params(self):
        param_dict = self.parent.params \
            if self.parent is not None else {}
        for name, param in self.data.get("with", {}).items():
            param_dict[name] = param
        for name, param in self._collection._params.items():
            param_dict[name] = param
        return param_dict

    @property
    def given(self):
        return self._precondition_dict

    @property
    def steps(self):
        return self._steps

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

    def documentation(self, template="story"):
        return utils.render_template(
            self._collection._templates,
            template,
            {"story": self, }
        )

    def play(self):
        """
        Run a story from beginning to end, time it and return
        a Result object.
        """
        start_time = time.time()
        self._collection.log(
            "RUNNING {0} in {1} ... ".format(
                self.name,
                self._story_file.filename,
            ),
            newline=False,
        )
        passed = False
        caught_exception = None
        try:
            from signal import signal, SIGINT, SIGTERM, SIGHUP, SIGQUIT

            signal(SIGINT, self.engine.on_abort)
            signal(SIGTERM, self.engine.on_abort)
            signal(SIGHUP, self.engine.on_abort)
            signal(SIGQUIT, self.engine.on_abort)

            current_step = None
            self.engine._preconditions = self.given
            self.engine.story = self
            self.engine.set_up()

            for step in self.steps:
                current_step = step
                self.engine.current_step = current_step
                run_step_method = step.method()
                run_step_method()

                if hasattr(self.engine, '_aborted') and self.engine._aborted:
                    self._collection.log("Aborted")
                    self.run_special_method(self.engine.tear_down, exceptions.TearDownException)
                    return
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
            self._collection.log(
                "SUCCESS in {0:.1f} seconds.".format(result.duration)
            )
        else:
            result = Failure(
                self,
                time.time() - start_time,
                caught_exception,
                current_step,
                failure_stack_trace,
            )
            self.run_on_failure(result)
            self._collection.log(
                (
                    "{red}{bright}FAILED in {duration:.1f} seconds.{reset_all}"
                    "\n\n{blue}{story_snippet}{reset_all}\n{stacktrace}"
                ).format(
                    red=colorama.Fore.RED,
                    bright=colorama.Style.BRIGHT,
                    duration=result.duration,
                    blue=colorama.Fore.BLUE,
                    reset=colorama.Fore.RESET,
                    reset_all=colorama.Style.RESET_ALL,
                    story_snippet=result.story_failure_snippet,
                    stacktrace=result.stacktrace,
                )
            )

        self.run_special_method(self.engine.tear_down, exceptions.TearDownException)
        return result

    def __repr__(self):
        return u"Story('{0}')".format(self._slug)
