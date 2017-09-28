Invalid story collections:
  preconditions:
    setup: |
      from hitchstory import StoryCollection, BaseEngine
  variations:
    Should be a list or iterator:
      preconditions:
        code: |
          StoryCollection("invalid", BaseEngine()).one().play()
      scenario:
      - Raises exception: storypaths should be a list or iterator returning a list
          of story files (e.g. using pathquery). Instead it was string 'invalid'.

    Nonexistent files:
      preconditions:
        code: |
          StoryCollection(["nonexistent", ], BaseEngine()).one().play()
      scenario:
      - Raises exception: Story file name 'nonexistent' does not exist.

    Is a directory, not a .story file:
      preconditions:
        code: |
          StoryCollection([".", ], BaseEngine()).one().play()
      scenario:
      - Raises exception: Story path '.' is a directory.
