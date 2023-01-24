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
        return [
            method.replace("_", " ")
            for method in self._engine.__class__.__dict__.keys()
            if not method.startswith("_") and method not in BaseEngine.__dict__.keys()
        ]

    def parse(self):
        self._parsed = load(
            self._doc_yaml_template,
            Map(
                {
                    "story": Str(),
                    Optional("variation"): Str(),
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

    def _render(self, name, template, variables):
        if template is not None:
            try:
                return self.jenv.from_string(template).render(**variables)
            except Exception:
                stack_trace = current_stack_trace_data()
                raise DocumentationTemplateError(
                    EXCEPTION_TEMPLATE.format(
                        name=name,
                        exception_type=stack_trace["exception_type"],
                        exception_message=stack_trace["exception_string"],
                    )
                )
        else:
            return ""

    def variation(self, **variables):
        return self._render(
            name="variation",
            template=self._parsed.get("variation"),
            variables=variables,
        )

    def story(self, **variables):
        return self._render(
            name="story", template=self._parsed["story"], variables=variables
        )

    def info_from_name(self, name, info_property):
        return self._render(
            name=f"info/{name}",
            template=self._parsed.get("info", {}).get(name),
            variables={name: info_property},
        )

    def given_from_name(self, name, given_property):
        return self._render(
            name=f"given/{name}",
            template=self._parsed.get("given", {}).get(name),
            variables={name: given_property},
        )

    def step_from_slug(self, slug, arguments):
        return self._render(
            name=f"steps/{slug}",
            template=self._slugified_steps.get(slug),
            variables=arguments,
        )
