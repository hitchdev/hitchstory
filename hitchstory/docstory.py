"""Documentation objects for use in templates."""
from hitchstory.step_method import StepMethod


class DocInfoProperty(object):
    def __init__(self, templates, name, info_property):
        self._templates = templates
        self._name = name
        self._info_property = info_property

    def documentation(self):
        return self._templates.info_from_name(self._name).render(
            **{self._name: self._info_property}
        )


class DocGivenProperty(object):
    def __init__(self, templates, name, given_property):
        self._templates = templates
        self._name = name
        self._given_property = given_property

    def documentation(self):
        return self._templates.given_from_name(self._name).render(
            **{self._name: self._given_property}
        )


class DocGivenProperties(object):
    def __init__(self, templates, given):
        self._templates = templates
        self._given = given

    def items(self):
        return [
            (name, DocGivenProperty(self._templates, name, given_property))
            for name, given_property in self._given.items()
        ]


class DocStep(object):
    def __init__(self, templates, step):
        self._templates = templates
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

        return self._templates.step_from_slug(self._step.slug).render(**arguments)
