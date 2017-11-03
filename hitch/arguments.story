Arguments to steps:
  description: |
    Arguments are fed to steps in a way that is
    largely consistent with how python methods work:

    * Named arguments are slugified to underscore_case.
    * kwargs are fed raw.
  given:
    engine.py: |
      from code_that_does_things import fill_form
      from hitchstory import BaseEngine

      class Engine(BaseEngine):
          def fill_form(self, **kwargs):
              for name, content in kwargs.items():
                  fill_form(name, content)
    setup: |
      from hitchstory import StoryCollection
      from engine import Engine
      from pathquery import pathq

  variations:
    kwargs:
      given:
        example.story: |
          Create files:
            steps:
              - Fill form:
                  login username: john
                  login password: hunter2
      steps:
      - Run:
          code: |
            result = StoryCollection(pathq(".").ext("story"), Engine()).named("Create files").play()
            print(result.report())
          will output: 'STORY RAN SUCCESSFULLY /path/to/example.story: Create files
            in 0.1 seconds.'

      - Form filled:
          login username: john
          login password: hunter2
