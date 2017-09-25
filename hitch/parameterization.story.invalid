Story with parameters:
  description: |
    Parameterized stories are used to describe stories
    which are essentially the same except for one or more
    things which change.
    
    A good example is a story for a user to log in with
    a browser which may be done with a number of different
    browsers - the parameter.
    
    Parameters can be used in preconditions and in steps.
  preconditions:
    example.story: |
      Click magic button:
        preconditions:
          browser: (( browser ))
        scenario:
          - Click on button
        default:
          browser:
            name: internet explorer
            version: 11
    engine.py: |
      from hitchstory import BaseEngine, StorySchema, validate
      from strictyaml import Map, Seq, Int, Str, Optional
      from code_that_does_things import *

      class Engine(BaseEngine):
          schema = StorySchema(
              preconditions=Map({
                  Optional("browser"): Map({"name": Str(), "version": Int()}),
              }),
          )
          
          def setup(self):
              append(self.preconditions['browser']['name'])
              append(self.preconditions['browser']['version'])

          def click_on_button(self):
              append("clicked!")

    setup: |
      from hitchstory import StoryCollection
      from pathquery import pathq
      from engine import Engine
    code: |
      print(StoryCollection(pathq(".").ext("story"), Engine()).one().play().report())

  variations:
    Default:
      scenario:
        - Run code
        - Output is: |
            internet explorer
            11
            clicked!
