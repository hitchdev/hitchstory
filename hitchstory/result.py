from hitchstory.utils import TEMPLATE_DIR
from jinja2.environment import Environment
from jinja2 import FileSystemLoader
import colorama


class FlakeResult(object):
    def __init__(self):
        self._results = []

    def append(self, result):
        self._results.append(result)

    @property
    def is_flaky(self):
        return self.failure_count > 0 and self.failure_count < self.total_results

    @property
    def failure_count(self):
        return len([result for result in self._results if not result.passed])

    @property
    def total_results(self):
        return len(self._results)

    @property
    def percentage_failures(self):
        return 100.0 * (float(self.failure_count) / float(self.total_results))


class ResultList(object):
    def __init__(self):
        self._results = []

    def append(self, result):
        self._results.append(result)

    @property
    def all_passed(self):
        return all([result.passed for result in self._results])

    def report(self):
        return "\n".join([result.report() for result in self._results])


class Report(object):
    pass


class Result(object):
    def _template(self, template_name):
        env = Environment()
        env.loader = FileSystemLoader(TEMPLATE_DIR)
        return env.get_template(
            str(TEMPLATE_DIR.joinpath(template_name).basename())
        ).render(
            result=self, Fore=colorama.Fore, Back=colorama.Back, Style=colorama.Style
        )

    @property
    def exit_code(self):
        return 0

    @property
    def passed(self):
        return True

    @property
    def duration(self):
        return self._duration

    @property
    def story(self):
        return self._story


class Success(Result):
    def __init__(self, story, duration):
        self._story = story
        self._duration = duration

    def report(self):
        return self._template("success.jinja2")


class FailureException(object):
    def __init__(self, exception):
        self._exception = exception

    @property
    def obj(self):
        return self._exception

    @property
    def obj_type(self):
        return str(self._exception.__class__.__name__)

    @property
    def docstring(self):
        return str(self._exception.__doc__)

    @property
    def text(self):
        return str(self._exception)


class Failure(Result):
    def __init__(self, story, duration, exception, failing_step, stacktrace):
        assert isinstance(exception, (Exception, RuntimeError))
        self._story = story
        self._duration = duration
        self._exception = FailureException(exception)
        self._failing_step = failing_step
        self._stacktrace = stacktrace

    @property
    def exit_code(self):
        return 1

    @property
    def passed(self):
        return False

    @property
    def exception(self):
        return self._exception

    @property
    def stacktrace(self):
        return self._stacktrace

    @property
    def story_failure_snippet(self):
        """
        Snippet of YAML highlighting the failing line.
        """
        if self._failing_step is None:
            return ""
        else:
            snippet = "{before}\n{bright}{lines}{normal}\n{after}".format(
                before=self._failing_step.yaml.lines_before(2),
                lines=self._failing_step.yaml.lines(),
                after=self._failing_step.yaml.lines_after(2),
                bright=colorama.Style.BRIGHT,
                normal=colorama.Style.NORMAL,
            )
            indented_snippet = "    " + snippet.replace("\n", "\n    ")
            return indented_snippet

    def to_dict(self):
        return {
            "story": self.story.to_dict(),
            "step": self.step.to_dict() if self.step else None,
            "exception": str(self.exception),
            "exception_type": "{}.{}".format(
                type(self.exception).__module__, type(self.exception).__name__
            ),
        }

    def report(self):
        return self._template("failure.jinja2")
