Story with given preconditions:
  about: |
    All stories start with an opening set of preconditions.

    In hitchstory, you can define this opening by with the
    'given' properties on a story. These are available
    at any time during the in the engine by referring to
    self.given, but are typically used in the set_up method
    to create the environment that the story is played in.

    The structure of the properties are defined using
    StorySchema.
  given:
    example.story: |
      Create files:
        given:
          thing:
            content: things
        steps:
          - Create file
    engine.py: |
      from hitchstory import BaseEngine, StorySchema
      from strictyaml import Str, Map, MapPattern

      def output(contents):
          with open("output.txt", 'a') as handle:
              handle.write("{0}\n".format(contents))

      class Engine(BaseEngine):
          schema=StorySchema(
              given={"thing": MapPattern(Str(), Str())},
          )

          def create_file(self):
              assert type(self.given['thing']['content']) is str
              assert type(list(self.given.keys())[0]) is str
              output(self.given['thing']['content'])
    setup: |
      from hitchstory import StoryCollection
      from pathquery import pathq
      from engine import Engine
  steps:
  - Run:
      code: |
        StoryCollection(pathq(".").ext("story"), Engine()).one().play()
      will output: |-
        RUNNING Create files in /path/to/example.story ... SUCCESS in 0.1 seconds.
  - File contents will be:
      filename: output.txt
      contents: things
