Attempt inheritance from non-existent story:
  given:
    core files:
      example.story: |
        Write to file:
          based on: Create files
          steps:
            - Do thing two
    setup: |
      from hitchstory import StoryCollection, BaseEngine
      from strictyaml import Map, Str
      from pathlib import Path


      class Engine(BaseEngine):
          def do_thing_one(self):
              print("thing one")

          def do_thing_two(self):
              print("thing two")

  steps:
  - Run:
      code: StoryCollection(Path(".").glob("*.story"), Engine()).named("Write to file").play()
      raises:
        type: hitchstory.exceptions.BasedOnStoryNotFound
        message: Story 'Create files' which 'Write to file' in '/path/to/working/example.story'
          is based upon not found.
