from hitchstory import utils
from collections import OrderedDict
import jinja2


class GivenProperty(object):
    def __init__(self, value, documentation):
        self._value = value
        self._documentation = documentation

    @property
    def value(self):
        return self._value

    @property
    def documentation(self):
        return self._documentation


class GivenProperties(object):
    def __init__(self, given):
        self._given = given

        self._properties = OrderedDict()
        for name, precondition in self._given.items():
            self._properties[name] = GivenProperty(
                precondition,
                jinja2.Template(self._given._document_templates[name]).render(
                    **{name: precondition}
                ),
            )

    def items(self):
        return self._properties.items()


class Given(object):
    def __init__(self, preconditions, document_templates=None):
        self._preconditions = preconditions
        self._document_templates = document_templates

    def get(self, key, default=None):
        return self._preconditions.get(utils.underscore_slugify(key), default)

    def __getitem__(self, key):
        slug = utils.underscore_slugify(key)

        if slug in self._preconditions:
            return self._preconditions[slug]
        else:
            raise KeyError(
                (
                    "'{}' / '{}' not found from given. Preconditions available: {}"
                ).format(
                    key,
                    slug,
                    ", ".join(self._preconditions.keys())
                    if len(self._preconditions.keys()) > 0
                    else "None",
                )
            )

    def __contains__(self, key):
        return utils.underscore_slugify(key) in self._preconditions.keys()

    def keys(self):
        return self._preconditions.keys()

    def items(self):
        return self._preconditions.items()

    def values(self):
        return self._preconditions.values()

    @property
    def properties(self):
        return GivenProperties(self)
