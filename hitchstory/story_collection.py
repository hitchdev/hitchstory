from hitchstory.story_list import StoryList
from hitchstory.story_file import StoryFile
from hitchstory.doc_template import DocTemplate
from hitchstory.engine import BaseEngine
from collections import OrderedDict
from hitchstory import exceptions
from slugify import slugify
from path import Path
from copy import copy
import io
import sys


class StoryCollection(object):
    """
    Unordered group of related stories.
    """

    def __init__(self, storypaths, engine):
        """
        Create a collection of hitch stories from a list (or generator) of
        story paths and an initialized story engine.
        """
        if not isinstance(engine, BaseEngine):
            raise exceptions.WrongEngineType(
                "Engine should inherit from hitchstory.BaseEngine."
            )
        if isinstance(storypaths, str):
            raise exceptions.InvalidStoryPaths(
                (
                    "storypaths should be a list or iterator returning a list of story files"
                    " (e.g. using pathlib.Path.glob). Instead it was string '{0}'."
                ).format(storypaths)
            )
        self._storypaths = storypaths
        self._engine = engine
        self._in_filename = None
        self._named = None
        self._filters = []
        self._params = {}
        self._story_files = {}
        self._filtered_stories = None
        self._non_variations = False
        self._only_uninherited = False
        self._templates = {}
        self._output_handle = sys.stdout
        self._flakecheck_times = None
        self._doc_templates = None
        self._external_test_runner = False

    @property
    def engine(self):
        return self._engine

    def story_file(self, filename):
        return StoryFile(filename, self)

    @property
    def stories(self):
        story_dict = OrderedDict()
        for filename in self._storypaths:
            if not Path(filename).exists():
                raise exceptions.InvalidStoryPaths(
                    "Story file name '{0}' does not exist.".format(filename)
                )
            if Path(filename).isdir():
                raise exceptions.InvalidStoryPaths(
                    "Story path '{0}' is a directory.".format(filename)
                )
            for story in self.story_file(filename).ordered_by_file():
                if story.slug in story_dict:
                    raise exceptions.DuplicateStoryNames(story, story_dict[story.slug])
                story_dict[story.slug] = story

        # Make sure parent stories know who their children are and vice versa
        for name, story in story_dict.items():
            if story.based_on is not None:
                parent_slug = slugify(story.based_on)

                if parent_slug not in story_dict:
                    raise exceptions.BasedOnStoryNotFound(
                        story.based_on, story.name, story.filename
                    )
                story_dict[parent_slug].children.append(story)
                story._parent = story_dict[parent_slug]

        # Revalidate steps and parameterize
        # These things can only be done after the story hierarchy is set
        for story in story_dict.values():
            story.initialize()
        return story_dict

    def ordered_by_file(self):
        """
        Return a StoryList containing stories filtered from the
        collection.

        The stories are primarily ordered according to the file
        ordering given to the story collection and secondarily
        according to the order they appear in those files.
        """
        return StoryList(self.ordered_arbitrarily())

    def ordered_arbitrarily(self):
        """
        Return a StoryList object containing stories filtered
        from the collection.
        """
        if self._filtered_stories is None:
            self._filtered_stories = []
            all_stories = []
            for story in self.stories.values():
                filtered = True
                for filter_func in self._filters:
                    if not filter_func(story):
                        filtered = False
                if self._named is not None:
                    if story.name != self._named:
                        filtered = False
                if self._in_filename is not None:
                    if (
                        Path(story.filename).abspath()
                        != Path(self._in_filename).abspath()
                    ):
                        filtered = False
                if self._non_variations:
                    if story.variation:
                        filtered = False
                if self._only_uninherited:
                    if len(story.children) > 0:
                        filtered = False
                if filtered:
                    self._filtered_stories.append(story)
                all_stories.append(story)
        return self._filtered_stories

    def filter(self, filter_func):
        assert callable(filter_func)
        new_collection = self.copy()
        new_collection._filters.append(filter_func)
        return new_collection

    def in_filename(self, filename):
        new_collection = self.copy()
        new_collection._in_filename = Path(filename)
        if not new_collection._in_filename.exists():
            raise exceptions.FileNotFound(filename)
        return new_collection

    def with_params(self, **params):
        new_collection = self.copy()
        new_collection._params = params
        return new_collection

    def without_filters(self):
        new_collection = self.copy()
        new_collection._filters = []
        return new_collection

    def in_any_filename(self):
        new_collection = self.copy()
        new_collection._in_filename = None
        return new_collection

    def non_variations(self):
        new_collection = self.copy()
        new_collection._non_variations = True
        return new_collection

    def only_uninherited(self):
        new_collection = self.copy()
        new_collection._only_uninherited = True
        return new_collection

    def with_flake_detection(self, times=5):
        new_collection = self.copy()
        new_collection._flakecheck_times = times
        return new_collection

    def with_templates(self, templates):
        new_collection = self.copy()
        new_collection._templates = templates
        return new_collection

    def with_documentation(self, yaml_documentation, extra=None):
        new_collection = self.copy()
        doc_template = DocTemplate(self.engine, yaml_documentation, extra)
        doc_template.parse()
        new_collection._doc_templates = doc_template
        return new_collection

    def with_external_test_runner(self):
        new_collection = self.copy()
        new_collection._output_handle = io.StringIO()
        new_collection._external_test_runner = True
        return new_collection

    def copy(self):
        new_collection = copy(self)
        new_collection._filtered_stories = None
        new_collection._stories = None

        for story in new_collection._story_files.values():
            story._collection = self
        return new_collection

    def named(self, name):
        """
        Return a single story object with the name specified.

        Only slugified names are compared. E.g. "Story NAME" and "story-name" are equivalent.
        """
        slug = slugify(name)
        for story in self.ordered_arbitrarily():
            if slug == story.slug:
                return story
        raise exceptions.StoryNotFound(name)

    def ordered_by_name(self):
        """
        Return a list of stories ordered by name.
        """
        return StoryList(
            sorted(self.ordered_arbitrarily(), key=lambda story: story.name)
        )

    def shortcut(self, *words):
        """
        Return a single story that matches all of the words.
        """
        matching = []
        stories = self.ordered_by_name()
        slugified_words = [slugify(word) for word in words]
        for story in stories:
            if len(words) == len(
                [
                    slugified_word
                    for slugified_word in slugified_words
                    if slugified_word in story.slug
                ]
            ):
                matching.append(story)
        if len(matching) == 0:
            raise exceptions.StoryNotFound(", ".join(words))
        elif len(matching) > 1:
            raise exceptions.MoreThanOneStory(
                "\n".join(
                    [
                        "{0} (in {1})".format(story.name, story.filename)
                        for story in matching
                    ]
                )
            )
        else:
            return matching[0]

    def log(self, message, newline=True):
        """
        Log message to the output handle (usually stdout).
        """
        self._output_handle.write("{0}{1}".format(message, "\n" if newline else ""))
        self._output_handle.flush()

    def one(self):
        stories = self.ordered_by_name()
        if len(stories) > 1:
            raise exceptions.MoreThanOneStory(
                "\n".join(
                    [
                        "{0} (in {1})".format(story.name, story.filename)
                        for story in stories
                    ]
                )
            )
        elif len(stories) == 0:
            raise exceptions.NoStories()
        else:
            return stories[0]
