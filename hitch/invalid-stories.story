Invalid story collections:
  given:
    setup: |
      from hitchstory import StoryCollection, BaseEngine
  variations:
    Should be a list or iterator:
      steps:
      - Run:
          code: StoryCollection("invalid", BaseEngine()).one().play()
          raises:
            type: hitchstory.exceptions.InvalidStoryPaths
            message: storypaths should be a list or iterator returning a list of story
              files (e.g. using pathquery). Instead it was string 'invalid'.

    Nonexistent files:
      steps:
      - Run:
          code: StoryCollection(["nonexistent", ], BaseEngine()).one().play()
          raises:
            type: hitchstory.exceptions.InvalidStoryPaths
            message: Story file name 'nonexistent' does not exist.

    Is a directory, not a .story file:
      steps:
      - Run:
          code: StoryCollection([".", ], BaseEngine()).one().play()
          raises:
            type: hitchstory.exceptions.InvalidStoryPaths
            message: Story path '.' is a directory.
