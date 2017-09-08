Variations:
  description: |
    Some stories are very similar except for a few changed items. You
    can create substories within the same story in order to enumerate
    all of the possible permutations.
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
        variations:
          cat:
            params:
              myparameter: cat
    setup: |
      from hitchstory import StoryCollection, BaseEngine, StorySchema, validate
      from strictyaml import Map, Seq, Int, Str
      from pathquery import pathq
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

    code: |
      print(StoryCollection(pathq(".").ext("story"), Engine()).shortcut("cat").play().report())
  scenario:
  - Run code
  - Output is: |
      cat
      cat
      42
      frog