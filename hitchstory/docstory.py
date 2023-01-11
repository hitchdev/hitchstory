"""Documentation objects for use in templates."""
from hitchstory.step_method import StepMethod


class DocInfoProperty(object):
    def __init__(self, templates, name, info_property):
        self._templates = templates
        self._name = name
        self._info_property = info_property
        self._documentation = self._templates.info_from_name(
            self._name, self._info_property
        )

    def documentation(self):
        return self._documentation


class DocGivenProperty(object):
    def __init__(self, templates, name, given_property):
        self._templates = templates
        self._name = name
        self._given_property = given_property
        self._documentation = self._templates.given_from_name(
            self._name, self._given_property
        )

    def documentation(self):
        return self._documentation


class DocGivenProperties(object):
    def __init__(self, templates, given):
        self._templates = templates
        self._given = given
        self._property_docs = {
            name: DocGivenProperty(self._templates, name, self._given[name])
            for name, given_property in self._given.items()
        }

    def __getattr__(self, name):
        return self._property_docs[name]

    def items(self):
        return self._property_docs.items()


class DocStep(object):
    def __init__(self, templates, step):
        self._templates = templates
        self._step = step

        step_method = StepMethod(self._step.step_method)
        arguments = {name: None for name in step_method.argspec.args[1:]}

        if self._step.arguments.single_argument:
            var_name = step_method.argspec.args[1:][0]
            arguments[var_name] = self._step.arguments.data
        else:
            if step_method.argspec.keywords:
                var_name = step_method.argspec.keywords
                arguments[var_name] = self._step.arguments.data
            else:
                arguments.update(self._step.arguments.data)

        self._documentation = self._templates.step_from_slug(self._step.slug, arguments)

    def documentation(self):
        return self._documentation


def story_template(story, doc_templates):
    return doc_templates.story(
        info={
            name: DocInfoProperty(doc_templates, name, info_property)
            for name, info_property in story.info.items()
        },
        slug=story.slug,
        given=DocGivenProperties(doc_templates, story.given),
        name=story.name,
        about=story.about,
        steps=[DocStep(doc_templates, step) for step in story.steps],
    )
