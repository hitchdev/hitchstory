Story with parameters:
  description: |
    Parameters are used to describe stories which remain
    identical except for specified changed preconditions
    or steps.

    You can use them to perform property based testing
    or to inherit one story from another where there
    is a minor variation.

    Parameters can only be used in preconditions or in
    steps. If you wish to use a parameter in a step or
    a precondition, that precondition or step value
    *must* accept strings.
  preconditions:
    example.story: |
      Create files:
        preconditions:
          content: (( myparameter ))
          hierarchical content:
            x: 1
            y:
              - (( parameter2 ))
        scenario:
          - Do thing with precondition
          - Do other thing: (( myparameter ))
          - Do yet another thing
          - Do a fourth thing:
              animals:
                pond animal: (( parameter3 ))
        params:
          myparameter: dog
          parameter2: 42
          parameter3: frog
    engine.py: |
      from hitchstory import BaseEngine, StorySchema, validate
      from strictyaml import Map, Seq, Int, Str
      from code_that_does_things import *

      class Engine(BaseEngine):
          schema = StorySchema(
              preconditions=Map({
                  "content": Str(),
                  "hierarchical content": Map({
                      "x": Int(),
                      "y": Seq(Str()),
                  }),
              }),
              params=Map({
                  "myparameter": Str(),
                  "parameter2": Int(),
                  "parameter3": Str(),
              }),
          )

          def do_other_thing(self, parameter):
              assert type(parameter) is str
              append(parameter)

          def do_thing_with_precondition(self):
              assert type(self.preconditions['content']) is str
              append(self.preconditions['content'])

          def do_yet_another_thing(self):
              assert type(self.preconditions['hierarchical content']['y'][0]) is str
              append(self.preconditions['hierarchical content']['y'][0])

          @validate(animals=Map({"pond animal": Str()}))
          def do_a_fourth_thing(self, animals=None):
              assert type(animals['pond animal']) is str
              append(animals['pond animal'])
    setup: |
      from hitchstory import StoryCollection
      from pathquery import pathq
      from engine import Engine
    code: |
      print(StoryCollection(pathq(".").ext("story"), Engine()).one().play().report())
  scenario:
    - Run code
    - Output is: |
        dog
        dog
        42
        frog
