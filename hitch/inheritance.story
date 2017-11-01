Inherit one story from another:
  description: |
    You cannot break most software down into a series of
    individual linear behavioral stories. Software
    stories, however, often branch.

    While it would be possible to write out each individual
    story for every possible branch, this would result in a
    story suite that is non-DRY and much more work to maintain.

    Story inheritance allows you to base stories on other stories.
    The base story's preconditions will all be used while the
    child story's preconditions (if it has any) will override
    them.

    The same is so for story parameters.

    The base story's scenario will be executed before continuing
    with the child story's scenario.
  preconditions:
    example.story: |
      Write to file 1:
        with:
          a: 1
          b: 2
          c: 3
        given:
          a: (( a ))
          b: (( b ))
        steps:
          - Do thing one
          - Do thing three: (( c ))

      Write to file 2:
        based on: Write to file 1
        given:
          b: 3
        steps:
          - Do thing two

      Write to file 3:
        based on: Write to file 1
        with:
          a: 9
          c: 11
    setup: |
      from hitchstory import StoryCollection, BaseEngine, StorySchema, validate
      from strictyaml import Map, Int, Str, Optional
      from pathquery import pathq
      from code_that_does_things import *

      class Engine(BaseEngine):
          schema = StorySchema(
              given={
                  Optional("a"): Str(), Optional("b"): Str()
              },
          )

          def do_thing_one(self):
              append("thing one: {0}, {1}".format(self.given['a'], self.given['b']))

          @validate(value=Str())
          def do_thing_three(self, value):
              append("thing three: {0}".format(value))

          def do_thing_two(self):
              assert isinstance(self.given['a'], str)
              assert isinstance(self.given['b'], str)
              append("thing two: {0}, {1}".format(self.given['a'], self.given['b']))

      collection = StoryCollection(pathq(".").ext("story"), Engine())
  variations:
    Original story:
      preconditions:
        code: |
          collection.named("Write to file 1").play()
      scenario:
      - Run code
      - Output is: |
          thing one: 1, 2
          thing three: 3

    Override preconditions:
      preconditions:
        code: |
          print(collection.named("Write to file 2").play().report())
      scenario:
      - Run code
      - Output is: |
          thing one: 1, 3
          thing three: 3
          thing two: 1, 3

    Override parameters:
      preconditions:
        code: |
          collection.named("Write to file 3").play()
      scenario:
      - Run code
      - Output is: |
          thing one: 9, 2
          thing three: 11



Attempt inheritance from non-existent story:
  preconditions:
    example.story: |
      Write to file:
        based on: Create files
        steps:
          - Do thing two
    setup: |
      from hitchstory import StoryCollection, BaseEngine
      from code_that_does_things import *
      from strictyaml import Map, Str
      from pathquery import pathq


      class Engine(BaseEngine):
          def do_thing_one(self):
              output("thing one")

          def do_thing_two(self):
              output("thing two")
    code: |
      StoryCollection(pathq(".").ext("story"), Engine()).named("Write to file").play()
  scenario:
  - Raises exception:
      exception type: hitchstory.exceptions.BasedOnStoryNotFound
      message: Story 'Create files' which 'Write to file' in '/path/to/example.story'
        is based upon not found.
