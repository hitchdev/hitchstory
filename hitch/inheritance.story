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
    files:
      example.story: |
        Write to file 1:
          preconditions:
            a: (( a ))
            b: (( b ))
          scenario:
            - Do thing one
            - Do thing three: (( c ))
          params:
            a: 1
            b: 2
            c: 3

        Write to file 2:
          based on: Write to file 1
          preconditions:
            b: 3
          scenario:
            - Do thing two

        Write to file 3:
          based on: Write to file 1
          params:
            a: 9
            c: 11
  scenario:
    - Run command: |
        from hitchstory import StoryCollection, BaseEngine, StorySchema
        from strictyaml import Map, Int, Str
        from pathquery import pathq
        from code_that_does_things import *

        class Engine(BaseEngine):
            schema = StorySchema(
                preconditions=Map({
                    "a": Str(), "b": Str()
                }),
                params=Map({
                    "a": Str(), "b": Str(), "c": Str()
                }),
            )

            def do_thing_one(self):
                append("thing one: {0}, {1}".format(self.preconditions['a'], self.preconditions['b']))

            def do_thing_three(self, value):
                append("thing three: {0}".format(value))

            def do_thing_two(self):
                append("thing two: {0}, {1}".format(self.preconditions['a'], self.preconditions['b']))

    - Run Command: StoryCollection(pathq(".").ext("story"), Engine()).named("Write to file 1").play()
    - Output is: |
        thing one: 1, 2
        thing three: 3

    - Run Command: StoryCollection(pathq(".").ext("story"), Engine()).named("Write to file 2").play()
    - Output is: |
        thing one: 1, 3
        thing three: 3
        thing two: 1, 3

    - Run Command: StoryCollection(pathq(".").ext("story"), Engine()).named("Write to file 3").play()
    - Output is: |
        thing one: 9, 2
        thing three: 11



Attempt inheritance from non-existent story:
  preconditions:
    files:
      example.story: |
        Write to file:
          based on: Create files
          scenario:
            - Do thing two
  scenario:
    - Run command: |
        from hitchstory import StoryCollection, BaseEngine
        from strictyaml import Map, Str
        from pathquery import pathq


        class Engine(BaseEngine):
            def do_thing_one(self):
                output("thing one")

            def do_thing_two(self):
                output("thing two")

    - Assert Exception:
        command: StoryCollection(pathq(".").ext("story"), Engine()).named("Write to file").play()
        exception: StoryNotFound
