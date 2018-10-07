from hitchstory.result import ResultList
from hitchstory.story import Story
from copy import copy


class StoryList(object):
    """
    A sequence of stories ready to be played in order.
    """

    def __init__(self, stories):
        for story in stories:
            assert type(story) is Story
        self._stories = stories
        self._continue_on_failure = False

    def continue_on_failure(self):
        new_story_list = copy(self)
        new_story_list._continue_on_failure = True
        return new_story_list

    def play(self):
        results = ResultList()
        if len(self._stories) > 0:
            for story in self._stories:
                result = story.play()
                results.append(result)

                if hasattr(story.engine, "_aborted") and story.engine._aborted:
                    break

                if not result.passed and not self._continue_on_failure:
                    break
        else:
            print("No stories found")
        return results

    def __len__(self):
        return len(self._stories)

    def __getitem__(self, index):
        return self._stories[index]
