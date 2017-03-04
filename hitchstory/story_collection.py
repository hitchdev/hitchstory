from hitchstory.engine import BaseEngine
from hitchstory.story import StoryList
from hitchstory.story import StoryFile
from hitchstory import exceptions
from slugify import slugify
from path import Path
from copy import copy


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
            raise exceptions.InvalidStoryPaths((
                "storypaths should be a list or iterator returning a list of story files"
                " (e.g. using pathquery). Instead it was string '{0}'."
            ).format(storypaths))
        self._storypaths = storypaths
        self._engine = engine
        self._in_filename = None
        self._named = None
        self._filters = []

        self._stories = {}

        for filename in self._storypaths:
            if not Path(filename).exists():
                raise exceptions.InvalidStoryPaths(
                    "Story file name '{0}' does not exist.".format(filename)
                )
            if Path(filename).isdir():
                raise exceptions.InvalidStoryPaths(
                    "Story path '{0}' is a directory.".format(filename)
                )
            for story in StoryFile(filename, self._engine, self).ordered_arbitrarily():
                if slugify(story.name) in self._stories:
                    raise exceptions.DuplicateStoryNames(story, self._stories[slugify(story.name)])
                self._stories[slugify(story.name)] = story

    def ordered_arbitrarily(self):
        """
        Return a StoryList object containing stories filtered
        from the collection.
        """
        stories = []
        for story in self._stories.values():
            filtered = True
            for filter_func in self._filters:
                if not filter_func(story):
                    filtered = False
            if self._named is not None:
                if story.name != self._named:
                    filtered = False
            if self._in_filename is not None:
                if Path(story.filename).abspath() != Path(self._in_filename).abspath():
                    filtered = False
            if filtered:
                stories.append(story)

        # Check for non-existent inherited stories
        for story in stories:
            if "based on" in story._parsed_yaml:
                inherited_from = story._parsed_yaml['based on']
                found = False
                for search_story in stories:
                    if inherited_from == search_story.name:
                        found = True
                if not found:
                    raise exceptions.StoryNotFound(inherited_from)
        return stories

    def filter(self, filter_func):
        assert callable(filter_func)
        new_collection = copy(self)
        new_collection._filters.append(filter_func)
        return new_collection

    def in_filename(self, filename):
        assert type(filename) is str
        new_collection = copy(self)
        new_collection._in_filename = Path(filename)
        assert new_collection._in_filename.exists()
        return new_collection

    def named(self, name):
        """
        Return a single story object with the name specified.

        Only slugified names are compared. E.g. "Story NAME" and "story-name" are equivalent.
        """
        for story in self.ordered_arbitrarily():
            if slugify(name) == story.slug:
                return story
        raise exceptions.StoryNotFound(name)

    def ordered_by_name(self):
        """
        Return a list of stories ordered by name.
        """
        return StoryList(sorted(self.ordered_arbitrarily(), key=lambda story: story.name))

    def shortcut(self, *words):
        """
        Return a single story that matches all of the words.
        """
        matching = []
        for story in self.ordered_arbitrarily():
            if len([word for word in words if slugify(word) in story.slug]) == len(words):
                matching.append(story)
        if len(matching) == 0:
            raise exceptions.StoryNotFound(", ".join(words))
        elif len(matching) > 1:
            raise exceptions.MoreThanOneStory(
                "\n".join([
                    "{0} (in {1})".format(story.name, story.filename) for story in matching
                ])
            )
        else:
            return matching[0]

    def one(self):
        stories = self.ordered_arbitrarily()
        if len(stories) > 1:
            raise exceptions.MoreThanOneStory(
                "\n".join([
                    "{0} (in {1})".format(story.name, story.filename) for story in stories
                ])
            )
        elif len(stories) == 0:
            raise exceptions.NoStories()
        else:
            return stories[0]
