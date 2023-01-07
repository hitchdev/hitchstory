"""Documentation objects for use in templates."""
from hitchstory.step_method import StepMethod


class DocInfoProperty(object):
    def __init__(self, docstory, name, info_property):
        self._docstory = docstory
        self._name = name
        self._info_property = info_property

    def documentation(self):
        return self._docstory.templates.info_from_name(self._name).render(
            **{self._name: self._info_property}
        )


class DocGivenProperty(object):
    def __init__(self, docstory, name, given_property):
        self._docstory = docstory
        self._name = name
        self._given_property = given_property

    def documentation(self):
        return self._docstory.templates.given_from_name(self._name).render(
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

    def documentation(self):
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

        return self._docstory.templates.step_from_slug(self._step.slug).render(
            **arguments
        )


class DocStory(object):
    def __init__(self, story):
        self.story = story

    def documentation(self):
        return self.templates.story.render(
            info={
                name: DocInfoProperty(self, name, info_property)
                for name, info_property in self.story.info.items()
            },
            slug=self.story.slug,
            given=DocGivenProperties(self),
            name=self.story.name,
            about=self.story.about,
            steps=[DocStep(self, step) for step in self.story.steps],
        )

    @property
    def templates(self):
        return self.story._collection._doc_templates
