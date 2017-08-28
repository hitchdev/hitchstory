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
        - Raises exception: should be a list or iterator
    
    Nonexistent files:
      preconditions:
        code: |
          StoryCollection(["nonexistent", ], BaseEngine()).one().play()
      scenario:
        - Raises exception: does not exist
    
    Is a directory, not a .story file:
      preconditions:
        code: |
          StoryCollection([".", ], BaseEngine()).one().play()
      scenario:
        - Raises exception: is a directory
