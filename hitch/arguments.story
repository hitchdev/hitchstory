Arguments to steps:
  docs: steps-and-step-arguments
  about: |
    Arguments are fed to steps in a way that is
    largely consistent with how python methods work:

    - Named arguments (e.g. "How many times") are put in equivalent named variables (e.g. "how_many_times").
    - If the method has **kwargs then the key names of kwargs will match the named arguments exactly (i.e. no underscores).
  given:
    engine.py: |
      from code_that_does_things import *
      from strictyaml import Int, Str, Bool
      from hitchstory import BaseEngine, validate

      class Engine(BaseEngine):
          def fill_form(self, **kwargs):
              for name, content in kwargs.items():
                  fill_form(name, content)

          @validate(what=Str(), how_many_times=Int(), double_click=Bool())
          def click(self, what, how_many_times=1, double_click=False):
              for _ in range(how_many_times):
                  click(what)
    setup: |
      from hitchstory import StoryCollection
      from engine import Engine
      from pathquery import pathquery

  variations:
    kwargs:
      given:
        example.story: |
          Login:
            steps:
              - Fill form:
                  login username: john
                  login password: hunter2
      steps:
      - Run:
          code: |
            StoryCollection(pathquery(".").ext("story"), Engine()).named("Login").play()
          will output: RUNNING Login in /path/to/example.story ... SUCCESS in 0.1
            seconds.   

      - Form filled:
          login username: john
          login password: hunter2

    optional args single argument:
      given:
        example.story: |
          Click button:
            steps:
              - Click: my button
      steps:
      - Run:
          code: |
            StoryCollection(pathquery(".").ext("story"), Engine()).named("Click button").play()
          will output: RUNNING Click button in /path/to/example.story ... SUCCESS
            in 0.1 seconds.

    optional args fewer than the maximum arguments:
      given:
        example.story: |
          Click button:
            steps:
              - Click:
                  what: my button
                  how many times: 2
      steps:
      - Run:
          code: |
            StoryCollection(pathquery(".").ext("story"), Engine()).named("Click button").play()
          will output: RUNNING Click button in /path/to/example.story ... SUCCESS
            in 0.1 seconds.
