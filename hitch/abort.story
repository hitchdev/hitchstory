Abort a story with ctrl-C:
  about: |
    When an in-progress story is hit with any of the
    following termination signals:

    * SIGTERM
    * SIGINT
    * SIGQUIT
    * SIGHUP

    Then it triggers the tear_down method of the
    engine.
    
    In practical terms this means that if you are running
    a series of stories, Ctrl-C should halt current execution,
    run tear_down and then not run any more stories.
  given:
    example.story: |
      Create files:
        steps:
          - Pause forever

      Should never run:
        steps:
          - Should not happen
    engine.py: |
      from hitchstory import BaseEngine
      from code_that_does_things import reticulate_splines
      import psutil

      class Engine(BaseEngine):
          def pause_forever(self):
              psutil.Process().terminate()

          def should_not_happen(self):
              raise Exception("This exception should never be triggered")

          def tear_down(self):
              reticulate_splines()
    setup: |
      from hitchstory import StoryCollection
      from pathquery import pathq
      from engine import Engine
  steps:
  - Run:
      code: StoryCollection(pathq(".").ext("story"), Engine()).ordered_by_name().play()
      will output: |-
        RUNNING Create files in /path/to/example.story ... Aborted
  - Splines reticulated
