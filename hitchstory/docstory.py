"""Documentation objects for use in templates."""
from jinja2 import Template
from slugify import slugify
from hitchstory.step_method import StepMethod
from hitchstory.utils import to_underscore_style
import jinja2


class DocInfoProperty(object):
    def __init__(self, docstory, name, info_property):
        self._docstory = docstory
        self._name = name
        self._info_property = info_property

    @property
    def documentation(self):
        return self._docstory.env.from_string(
            self._docstory.templates.info[self._name]
        ).render(**{self._name: self._info_property})


class DocGivenProperty(object):
    def __init__(self, docstory, name, given_property):
        self._docstory = docstory
        self._name = name
        self._given_property = given_property

    @property
    def documentation(self):
        return Template(self._docstory.templates.given[self._name]).render(
            **{self._name: self._given_property}
        )


class DocGivenProperties(object):
    def __init__(self, docstory):
        self._docstory = docstory

    def items(self):
        return [
            (name, DocGivenProperty(self._docstory, name, given_property))
            for name, given_property in self._docstory.story.given.items()
        ]


class DocStep(object):
    def __init__(self, docstory, step):
        self._docstory = docstory
        self._step = step

    @property
    def documentation(self):
        step_method = StepMethod(self._step.step_method)
        if self._step.arguments.single_argument:
            var_name = step_method.argspec.args[1:][0]
            return Template(
                self._docstory.slug_templates["steps"][self._step.slug]
            ).render(**{var_name: self._step.arguments.data})
        else:
            if step_method.argspec.keywords:
                var_name = step_method.argspec.keywords
                return Template(
                    self._docstory.slug_templates["steps"][self._step.slug]
                ).render(**{var_name: self._step.arguments.data})
            else:
                return Template(
                    self._docstory.slug_templates["steps"][self._step.slug]
                ).render(**self._step.arguments.data)


class DocStory(object):
    def __init__(self, story):
        self.env = jinja2.Environment(
            undefined=jinja2.StrictUndefined, loader=jinja2.BaseLoader
        )
        self.story = story
        self._slugified_templates = {
            "story": self.templates.story,
            "steps": {
                to_underscore_style(name): text
                for name, text in self.templates.steps.items()
            },
            "given": {
                slugify(name): text for name, text in self.templates.given.items()
            },
        }

    def documentation(self):
        return self.env.from_string(self.templates.story).render(
            info=self.info,
            given=self.given,
            name=self.name,
            about=self.about,
            steps=self.steps,
        )

    @property
    def slug(self):
        return self.story.slug

    @property
    def name(self):
        return self.story.name

    @property
    def about(self):
        return self.story.about

    @property
    def given(self):
        return DocGivenProperties(self)

    @property
    def info(self):
        return {
            name: DocInfoProperty(self, name, info_property)
            for name, info_property in self.story.info.items()
        }

    @property
    def steps(self):
        return [DocStep(self, step) for step in self.story.steps]

    @property
    def templates(self):
        return self.story._collection._doc_templates

    @property
    def slug_templates(self):
        return self._slugified_templates

    @property
    def variables(self):
        return {
            "about": self.templates.story,
            "steps": {
                to_underscore_style(name): text
                for name, text in self.templates.steps.items()
            },
            "given": {
                slugify(name): text for name, text in self.templates.given.items()
            },
        }

    def render(self):
        return self.env.from_string(self.templates.story).render(**self.variables)
