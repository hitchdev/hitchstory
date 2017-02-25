from jinja2.environment import Environment
from jinja2 import FileSystemLoader
from os import path
import colorama


TEMPLATE_DIR = path.join(path.dirname(path.realpath(__file__)), "templates")


class ResultList(object):
    def __init__(self):
        self._results = []

    def append(self, result):
        self._results.append(result)

    def report(self):
        return '\n'.join([result.report() for result in self._results])


class Report(object):
    pass


class Result(object):
    def _template(self, template_name):
        env = Environment()
        env.loader = FileSystemLoader(TEMPLATE_DIR)
        return env.get_template(
            path.basename(path.join(TEMPLATE_DIR, template_name))
        ).render(
            result=self,
            Fore=colorama.Fore,
            Back=colorama.Back,
            Style=colorama.Style,
        )

    @property
    def exit_code(self):
        return 0

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
        assert type(exception) is Exception or RuntimeError
        self._story = story
        self._duration = duration
        self._exception = FailureException(exception)
        self._failing_step = failing_step
        self._stacktrace = stacktrace

    @property
    def exit_code(self):
        return 1

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
            'story': self.story.to_dict(),
            'step': self.step.to_dict() if self.step else None,
            'exception': str(self.exception),
            'exception_type': "{}.{}".format(
                type(self.exception).__module__, type(self.exception).__name__
            ),
        }

    def report(self):
        return self._template("failure.jinja2")
