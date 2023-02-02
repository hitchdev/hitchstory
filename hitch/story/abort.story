Abort a story with ctrl-C:
  docs: aborting
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
    files:
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
                print("Reticulate splines")
    setup: |
      from hitchstory import StoryCollection
      from pathlib import Path
      from engine import Engine
  steps:
  - Run:
      code: StoryCollection(Path(".").glob("*.story"), Engine()).ordered_by_name().play()
      will output: |-
        RUNNING Create files in /path/to/working/example.story ... Aborted
        Reticulate splines
