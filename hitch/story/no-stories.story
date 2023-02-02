No stories:
  given:
    files:
      example.story: |
        # hello
        Example story
      engine.py: |
        from hitchstory import BaseEngine

        class Engine(BaseEngine):
            pass
  steps:
  - Run:
      code: |
        from hitchstory import StoryCollection
        from pathlib import Path
        from engine import Engine

        StoryCollection(Path(".").glob("*.story"), Engine()).ordered_by_name().play()
      will output: No stories found
