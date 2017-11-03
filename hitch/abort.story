Abort a story with ctrl-C:
  description: |
    When an in-progress story is hit with any of the
    following termination signals:

    * SIGTERM
    * SIGINT
    * SIGQUIT
    * SIGHUP

    Then it triggers the "on_abort" method of the
    engine, feeding it the signal number (integer)
    and stack frame.
  given:
    example.story: |
      Create files:
        steps:
          - Pause forever
    engine.py: |
      from hitchstory import BaseEngine
      from code_that_does_things import reticulate_splines
      import psutil


      class Engine(BaseEngine):
          def pause_forever(self):
              psutil.Process().terminate()

          def on_abort(self, signal_num, stack_frame):
              reticulate_splines()
    setup: |
      from hitchstory import StoryCollection
      from pathquery import pathq
      from engine import Engine
  steps:
  - Run:
      code: StoryCollection(pathq(".").ext("story"), Engine()).named("Create files").play()
  - Splines reticulated
