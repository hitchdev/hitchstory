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
    engine.py: "from hitchstory import BaseEngine, expected_exception, Failure\nfrom\
      \ code_that_does_things import *\n\n\nclass Engine(BaseEngine):\n    def passing_step(self):\n\
      \        pass\n    \n    def failing_step(self):\n        raise_example_exception(\"\
      Towel not located\")\n    \n    @expected_exception(ExampleException)\n    def\
      \ failing_step_without_stacktrace(self):\n        raise_example_exception(\"\
      Expected exception\")\n        \n    def raise_special_failure_exception(self):\n\
      \        raise Failure(\"Special failure exception - no stacktrace printed!\"\
      )\n    \n    def on_failure(self, result):\n        output(result.report())\n\
      \    \n    def not_executed_step(self):\n        pass\n"
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


    Expected exception:
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


    Special exception named failure:
      description: |
        If you want to indicate a test failure, raise the
        "Failure" exception.

        This is by default an expected exception, so no stack trace
        will be printed if it is raised.
      preconditions:
        example.story: |
          Failing story:
            scenario:
              - Raise special failure exception
        code: |
          StoryCollection(pathq(".").ext("story"), Engine()).one().play()
      scenario:
      - Run code
      - Output will be:
          reference: special exception failure
          changeable:
          - ((( anything )))/code_that_does_things.py
          - FAILURE IN ((( anything )))/example.story
          - ((( anything )))/story.py
          - ((( anything )))/engine.py

