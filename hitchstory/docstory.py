"""Documentation objects for use in templates."""
from hitchstory.step_method import StepMethod
import pathlib


class DocStory(object):
    def __init__(self, story):
        self.slug = story.slug
        self.name = story.name


class DocVariation(object):
    def __init__(self, templates, variables):
        self._documentation = templates.variation(**variables)

    def documentation(self):
        return self._documentation


class DocInfoProperty(object):
    def __init__(self, templates, name, info_property):
        self._documentation = templates.info_from_name(name, info_property)

    def documentation(self):
        return self._documentation


class DocGivenProperty(object):
    def __init__(self, templates, name, given_property):
        self._documentation = templates.given_from_name(name, given_property)

    def documentation(self):
        return self._documentation


class DocGivenProperties(object):
    def __init__(self, templates, given, child=False):
        self._property_docs = {
            name: DocGivenProperty(templates, name, given[name])
            for name, given_property in given.items()
        }
        if not child:
            self.child = DocGivenProperties(templates, given.child, child=True)

    def __getattr__(self, name):
        return self._property_docs[name]

    def items(self):
        return self._property_docs.items()


class DocStep(object):
    def __init__(self, templates, step, this_story):
        step_method = StepMethod(step.step_method)
        arguments = {name: None for name in step_method.argspec.args[1:]}

        if step.arguments.is_none:
            arguments = {}
        elif step.arguments.single_argument:
            var_name = step_method.argspec.args[1:][0]
            arguments[var_name] = step.arguments.data
        else:
            if step_method.argspec.keywords:
                var_name = step_method.argspec.keywords
                arguments[var_name] = step.arguments.data
            else:
                arguments.update(step.arguments.data)

        variables = dict(arguments)
        variables["this_step"] = self
        variables["this_story"] = this_story
        self._slug = step.slug
        self._index = step.index
        self._documentation = templates.step_from_slug(step.slug, variables)

    @property
    def slug(self):
        return self._slug

    @property
    def index(self):
        return self._index

    def documentation(self):
        return self._documentation


def _story_variables(story, doc_templates, variation=False):
    this_story = DocStory(story)
    variables = {
        "info": {
            name: DocInfoProperty(doc_templates, name, info_property)
            for name, info_property in story.info.items()
        },
        "slug": story.slug,
        "given": DocGivenProperties(doc_templates, story.given),
        "name": story.child_name if variation else story.name,
        "about": story.about,
        "steps": [DocStep(doc_templates, step, this_story) for step in story.steps],
        "filename": pathlib.Path(story.filename),
    }
    if variation:
        variables["full_name"] = story.name
    return variables


def story_template(story, doc_templates):
    variables = _story_variables(story, doc_templates)
    variables["variations"] = [
        DocVariation(
            doc_templates, _story_variables(variation, doc_templates, variation=True)
        )
        for variation in story.variations
    ]
    return doc_templates.story(**variables)
