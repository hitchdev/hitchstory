Simple failure report:
  description: |
    Basic failure report.
  preconditions:
    example.story: |
      Failing story:
        scenario:
          - Passing step
          - Failing step
          - Not executed step
    engine.py: |
      from hitchstory import BaseEngine, expected_exception
      from code_that_does_things import *


      class Engine(BaseEngine):
          def passing_step(self):
              pass

          def failing_step(self):
              raise_example_exception("Towel not located")
          
          @expected_exception(ExampleException)
          def failing_step_without_stacktrace(self):
              raise_example_exception("Expected exception")

          def on_failure(self, result):
              output(result.report())

          def not_executed_step(self):
              pass
    setup: |
      from hitchstory import StoryCollection
      from engine import Engine
      from pathquery import pathq

    code: |
      StoryCollection(pathq(".").ext("story"), Engine()).one().play()
  variations:
    Failure printed by on_failure method:
      scenario:
        - Run code
        - Output will be:
            reference: failure printed in on_failure
            changeable:
              - ((( anything )))/code_that_does_things.py
              - FAILURE IN ((( anything )))/example.story
              - ((( anything )))/story.py
              - ((( anything )))/engine.py
    
    Failure printed by default:
      preconditions:
        code: |
          StoryCollection(pathq(".").ext("story"), Engine()).one().play()
      scenario:
        - Run code
        - Output will be:
            reference: failure printed by default
            changeable:
              - ((( anything )))/code_that_does_things.py
              - FAILURE IN ((( anything )))/example.story
              - ((( anything )))/story.py
              - ((( anything )))/engine.py

      
    Failure expected exception:
      description: |
        For common expected failures where you do not want
        to see the whole stacktrace.
      preconditions:
        example.story: |
          Failing story:
            scenario:
              - Failing step without stacktrace
        code: |
          StoryCollection(pathq(".").ext("story"), Engine()).one().play()
      scenario:
        - Run code
        - Output will be:
            reference: failure with expected exception
            changeable:
              - ((( anything )))/code_that_does_things.py
              - FAILURE IN ((( anything )))/example.story
              - ((( anything )))/story.py
              - ((( anything )))/engine.py
