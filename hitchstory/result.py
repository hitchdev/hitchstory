from jinja2.environment import Environment
from jinja2 import FileSystemLoader
from os import path
import colorama
import json
import sys


TEMPLATE_DIR = path.join(path.dirname(path.realpath(__file__)), "templates")


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
    def story(self):
        return self._story

class Success(Result):
    def __init__(self, story):
        self._story = story
    
    def in_color(self):
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
    def __init__(self, story, exception):
        assert type(exception) is Exception or RuntimeError
        self._story = story
        self._exception = FailureException(exception)

    @property
    def exit_code(self):
        return 1

    @property
    def exception(self):
        return self._exception

    def to_dict(self):
        return {
            'story': self.story.to_dict(),
            'step': self.step.to_dict() if self.step else None,
            'exception': str(self.exception),
            'exception_type': "{}.{}".format(
                type(self.exception).__module__, type(self.exception).__name__
            ),
        }

    def in_color(self):
        env = Environment()
        env.loader = FileSystemLoader(TEMPLATE_DIR)
        return env.get_template(
            path.basename(path.join(TEMPLATE_DIR, "default.jinja2"))
        ).render(
            result=self,
            Fore=colorama.Fore,
            Back=colorama.Back,
            Style=colorama.Style,
        )

        #return "{}".format(self._exception)


    def report(self):
        env = Environment()
        env.loader = FileSystemLoader(TEMPLATE_DIR)
        tmpl = env.get_template(path.basename(template))
        return tmpl.render(
            stacktrace=self.to_dict(),
            #Fore=colorama.Fore,
            #Back=colorama.Back,
            #Style=colorama.Style,
        )

        return "{}".format(self._exception)
