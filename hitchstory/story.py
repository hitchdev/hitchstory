from hitchstory.utils import DEFAULT_STACK_TRACE, underscore_slugify
from hitchstory.result import Success, Failure, FlakeResult
from hitchstory.story_step import StoryStep
from hitchstory.given import Given
from hitchstory import exceptions
from hitchstory import docstory
from hitchstory import utils
from collections import OrderedDict
from slugify import slugify
import colorama
import time


class StoryInfo:
    def __init__(self, info_definition, data):
        self._info = OrderedDict()
        for info_property in info_definition.keys():
            if info_property in data.keys():
                self._info[underscore_slugify(info_property)] = data.get(
                    underscore_slugify(info_property)
                )

    def get(self, key, default=None):
        return self._info.get(underscore_slugify(key), default)

    def items(self):
        return self._info.items()

    def __getitem__(self, key):
        return self._info[underscore_slugify(key)]

    def __contains__(self, key):
        return underscore_slugify(key) in self._info.keys()


class Story(object):
    def __init__(self, story_file, name, parsed_yaml, variation_of=None):
        self._story_file = story_file
        self._name = name
        self._slug = None
        self._parsed_yaml = parsed_yaml
        self._steps = []
        self._parent = None
        self._variation_of = variation_of
        self._info = StoryInfo(self.engine.info_definition, self.data)
        self._collection = self._story_file.collection
        self.children = []
        self.about = self.data.get("about", "")

    def _unparameterized_preconditions(self):
        precondition_dict = (
            self.parent._unparameterized_preconditions()
            if self.parent is not None
            else OrderedDict()
        )
        for name, precondition in self.data.get("given", OrderedDict()).items():
            precondition_dict[name] = precondition
        return precondition_dict

    @property
    def _yaml_steps(self):
        step_list = self._parent_steps
        step_list.extend(self._parsed_yaml.get("steps", []))
        return step_list

    @property
    def _parent_steps(self):
        return self.parent._yaml_steps if self.parent is not None else []

    def _parameterized_preconditions(self, unparameterized_preconditions):
        all_preconditions = unparameterized_preconditions

        for name, precondition in all_preconditions.items():
            if utils.is_parameter(precondition):
                all_preconditions[name] = self.params[
                    utils.parameter_name(precondition)
                ]
            else:
                all_preconditions[name] = precondition
        return all_preconditions

    def initialize(self):
        """
        Revalidate steps and parameterize stories.
        These things can only be done after the story hierarchy is set
        """
        all_paramaterized_preconditions = self._parameterized_preconditions(
            self._unparameterized_preconditions()
        )

        self._given = Given(
            all_paramaterized_preconditions,
            self.engine.given_definition.document_templates,
        )

        number_of_parent_steps = len(self._parent_steps)

        self._steps = [
            StoryStep(
                self, parsed_step, index, index - number_of_parent_steps, self.params
            )
            for index, parsed_step in enumerate(self._yaml_steps)
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
        return self.data["based_on"] if "based_on" in self.data else self._variation_of

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
        return (
            self._name
            if not self.variation
            else "{0}/{1}".format(self._variation_of, self._name)
        )

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
        param_dict = self.parent.params if self.parent is not None else {}
        for name, param in self.data.get("with", {}).items():
            param_dict[name] = param
        for name, param in self._collection._params.items():
            param_dict[name] = param
        return param_dict

    @property
    def given(self):
        return self._given

    @property
    def steps(self):
        return self._steps

    def _run_special_method(self, method, exception_to_raise, result=None):
        try:
            if result is None:
                method()
            else:
                method(result)
        except Exception:
            stack_trace = DEFAULT_STACK_TRACE.current_stacktrace()

            raise exception_to_raise(stack_trace)

    def _run_on_success(self):
        try:
            self.engine.on_success()
        except Exception:
            self._run_special_method(
                self.engine.tear_down, exceptions.TearDownException
            )
            stack_trace = DEFAULT_STACK_TRACE.current_stacktrace()

            raise exceptions.OnSuccessException(stack_trace)

    def _run_on_failure(self, result):
        try:
            self.engine.on_failure(result)
        except Exception:
            self._run_special_method(
                self.engine.tear_down, exceptions.TearDownException
            )
            stack_trace = DEFAULT_STACK_TRACE.current_stacktrace()

            raise exceptions.OnFailureException(stack_trace)

    def _play_single_story(self):
        start_time = time.time()
        self._collection.log(
            "RUNNING {0} in {1} ... ".format(self.name, self._story_file.filename),
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
            self.engine._given = self.given
            self.engine.story = self
            self.engine.set_up()

            for step in self.steps:
                current_step = step
                self.engine.current_step = current_step
                run_step_method = step.method()
                run_step_method()

                if hasattr(self.engine, "_aborted") and self.engine._aborted:
                    self._collection.log("Aborted")
                    self._run_special_method(
                        self.engine.tear_down, exceptions.TearDownException
                    )
                    return
            passed = True
        except Exception as exception:
            caught_exception = exception
            if current_step is not None and current_step.expect_exception(
                self.engine, caught_exception
            ):
                failure_stack_trace = (
                    DEFAULT_STACK_TRACE.only_the_exception().current_stacktrace()
                )
            else:
                failure_stack_trace = DEFAULT_STACK_TRACE.current_stacktrace()

        if passed:
            self._run_on_success()
            result = Success(self, time.time() - start_time)
            self.story_file.rewrite()
            self._collection.log(
                "{green}SUCCESS{reset_all} in {duration:.1f} seconds.".format(
                    green=colorama.Fore.GREEN,
                    reset_all=colorama.Style.RESET_ALL,
                    duration=result.duration,
                )
            )
        else:
            result = Failure(
                self,
                time.time() - start_time,
                caught_exception,
                current_step,
                failure_stack_trace,
            )
            self._run_on_failure(result)
            self._collection.log(
                (
                    "{red}{bright}FAILED in {duration:.1f} seconds.{reset_all}"
                    "\n\n{blue}{story_snippet}{reset_all}\n{stacktrace}"
                ).format(
                    red=colorama.Fore.RED,
                    bright=colorama.Style.BRIGHT,
                    duration=result.duration,
                    blue=colorama.Fore.BLUE,
                    reset_all=colorama.Style.RESET_ALL,
                    story_snippet=result.story_failure_snippet,
                    stacktrace=result.stacktrace,
                )
            )

        self._run_special_method(self.engine.tear_down, exceptions.TearDownException)
        return result

    def documentation(self):
        """Generate textual documentation from story."""
        doc_templates = self._collection._doc_templates
        if doc_templates is None:
            raise exceptions.WithDocumentationMissing(
                "Documentation templates missing. Did you use .with_documentation?"
            )
        return docstory.story_template(self, doc_templates)

    def play(self):
        """
        Run a story from beginning to end, time it and return
        a Result object.
        """
        if self._collection._flakecheck_times is None:
            return self._play_single_story()
        else:
            start_time = time.time()
            result = FlakeResult()

            for i in range(self._collection._flakecheck_times):
                result.append(self._play_single_story())

            if result.is_flaky:
                self._collection.log(
                    "\nFLAKINESS DETECTED in {0:.1f} seconds, {1:.0f}% of stories failed.".format(
                        time.time() - start_time, result.percentage_failures
                    )
                )
                return result
            else:
                self._collection.log(
                    (
                        "\nNO FLAKINESS DETECTED in {duration:.1f} seconds "
                        "after running '{name}' story {count} times."
                    ).format(
                        duration=time.time() - start_time,
                        name=self.name,
                        count=result.total_results,
                    )
                )
                return result

    def __repr__(self):
        return "Story('{0}')".format(self._slug)
