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
  preconditions:
    files:
      example.story: |
        Create files:
          scenario:
            - Pause forever
      engine.py: |
        from hitchstory import BaseEngine
        from code_that_does_things import *
        import psutil


        class Engine(BaseEngine):
            def pause_forever(self):
                psutil.Process().terminate()

            def on_abort(self, signal_num, stack_frame):
                reticulate_splines()
  scenario:
    - Run command: |
        from hitchstory import StoryCollection
        from pathquery import pathq
        from engine import Engine

        result = StoryCollection(pathq(".").ext("story"), Engine()).named("Create files").play()
        output(result.report())
    - Splines reticulated
