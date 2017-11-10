from hitchstory.story_list import StoryList
from hitchstory.story_file import StoryFile
from hitchstory.engine import BaseEngine
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
        self._params = {}
        self._story_files = {}
        self._stories = None
        self._filtered_stories = None

    @property
    def engine(self):
        return self._engine

    def story_file(self, filename):
        if filename not in self._story_files:
            self._story_files[filename] = StoryFile(filename, self)
        return self._story_files[filename]

    @property
    def stories(self):
        if self._stories is None:
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
                for story in self.story_file(filename).ordered_arbitrarily():
                    if story.slug in self._stories:
                        raise exceptions.DuplicateStoryNames(story, self._stories[story.slug])
                    self._stories[story.slug] = story
        return self._stories

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
                    if Path(story.filename).abspath() != Path(self._in_filename).abspath():
                        filtered = False
                if filtered:
                    self._filtered_stories.append(story)
                all_stories.append(story)

            # Check for non-existent inherited stories
            for story in self._filtered_stories:
                if "based on" in story._parsed_yaml:
                    inherited_from = story._parsed_yaml['based on'].text
                    inherited_from_slug = slugify(inherited_from)
                    found = False
                    for search_story in all_stories:
                        if inherited_from_slug == search_story.slug:
                            found = True
                    if not found:
                        raise exceptions.BasedOnStoryNotFound(
                            inherited_from,
                            story.name,
                            story.filename,
                        )
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
        return StoryList(sorted(self.ordered_arbitrarily(), key=lambda story: story.name))

    def shortcut(self, *words):
        """
        Return a single story that matches all of the words.
        """
        matching = []
        stories = self.ordered_by_name()
        slugified_words = [slugify(word) for word in words]
        for story in stories:
            if len(words) == len([
                slugified_word for slugified_word in slugified_words
                if slugified_word in story.slug
            ]):
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
        stories = self.ordered_by_name()
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
