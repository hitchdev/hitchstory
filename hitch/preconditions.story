Story with preconditions:
  preconditions:
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
    code: |
      print(StoryCollection(pathq(".").ext("story"), Engine()).one().play().report())
  scenario:
  - Run code
  - Output is: things
