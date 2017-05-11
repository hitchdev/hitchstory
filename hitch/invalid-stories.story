Invalid file list:
  tags:
    - invalid-files
    - exception
  scenario:
    - Run command: |
        from hitchstory import StoryCollection, BaseEngine
    - Assert Exception:
        command: |
          result = StoryCollection("invalid", BaseEngine()).one().play()
        exception: should be a list or iterator
    - Assert Exception:
        command: |
          result = StoryCollection(["nonexistent", ], BaseEngine()).one().play()
        exception: does not exist
    - Assert Exception:
        command: |
          result = StoryCollection([".", ], BaseEngine()).one().play()
        exception: is a directory
