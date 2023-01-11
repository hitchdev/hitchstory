from strictyaml import Map, Str, Optional, load
from hitchstory.utils import to_underscore_style, current_stack_trace_data
from hitchstory.exceptions import DocumentationTemplateError
from hitchstory.engine import BaseEngine
import jinja2

EXCEPTION_TEMPLATE = """\
Exception in '{name}' template.

{exception_type}
{exception_message}
"""


class DocTemplate(object):
    def __init__(self, engine, doc_yaml_template, extra):
        self._doc_yaml_template = doc_yaml_template
        self.jenv = jinja2.Environment(
            undefined=jinja2.StrictUndefined, loader=jinja2.BaseLoader
        )
        if extra is not None:
            self.jenv.globals.update(extra)
        self._engine = engine

    def _step_methods(self):
        base_methods = [
            method
            for method in BaseEngine.__dict__.keys()
            if not method.startswith("_")
        ]
        return [
            method.replace("_", " ")
            for method in self._engine.__class__.__dict__.keys()
            if not method.startswith("_") and method not in base_methods
        ]

    def parse(self):
        self._parsed = load(
            self._doc_yaml_template,
            Map(
                {
                    "story": Str(),
                    Optional("given"): Map(
                        {
                            Optional(name): Str()
                            for name in self._engine.given_definition.keys()
                        }
                    ),
                    Optional("info"): Map(
                        {
                            Optional(name): Str()
                            for name in self._engine.info_definition.keys()
                        }
                    ),
                    Optional("steps"): Map(
                        {Optional(name): Str() for name in self._step_methods()}
                    ),
                }
            ),
        ).data

        self._slugified_steps = {
            to_underscore_style(name): text
            for name, text in self._parsed.get("steps", {}).items()
        }

    def validate(self):
        pass

    def story(self, **variables):
        try:
            return self.jenv.from_string(self._parsed["story"]).render(**variables)
        except Exception:
            stack_trace = current_stack_trace_data()
            raise DocumentationTemplateError(
                EXCEPTION_TEMPLATE.format(
                    name="story",
                    exception_type=stack_trace["exception_type"],
                    exception_message=stack_trace["exception_string"],
                )
            )

    def info_from_name(self, name, info_property):
        if "info" in self._parsed:
            try:
                return self.jenv.from_string(self._parsed["info"][name]).render(
                    **{name: info_property}
                )
            except Exception:
                stack_trace = current_stack_trace_data()
                raise DocumentationTemplateError(
                    EXCEPTION_TEMPLATE.format(
                        name="story",
                        exception_type=stack_trace["exception_type"],
                        exception_message=stack_trace["exception_string"],
                    )
                )
        else:
            return ""

    def given_from_name(self, name):
        return self.jenv.from_string(self._parsed["given"][name])

    def step_from_slug(self, slug):
        return self.jenv.from_string(self._slugified_steps[slug])
