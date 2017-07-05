Exception in on_success:
  preconditions:
    files:
      example.story: |
        Do thing:
          scenario:
            - Do thing
      engine.py: |
        from hitchstory import BaseEngine
        from code_that_does_things import *

        class Engine(BaseEngine):
            def do_thing(self):
                pass

            def on_success(self):
                raise_example_exception()
  scenario:
    - Run command: |
        from hitchstory import StoryCollection
        from pathquery import pathq
        from engine import Engine

    - Exception raised: 
        command: StoryCollection(pathq(".").ext("story"), Engine()).one().play()
        reference: exception in on_success
        changeable:
          - ~/((( anything )))/story.py
          - /((( anything )))/code_that_does_things.py
          - /((( anything )))/engine.py
          - <ipython-input-((( anything )))>

Exception in on_failure:
  preconditions:
    files:
      example.story: |
        Do thing:
          scenario:
            - Do thing
      engine.py: |
        from hitchstory import BaseEngine
        from code_that_does_things import *

        class Engine(BaseEngine):
            def do_thing(self):
                raise_example_exception()

            def on_failure(self):
                raise_example_exception()
  scenario:
    - Run command: |
        from hitchstory import StoryCollection
        from pathquery import pathq
        from engine import Engine

    - Exception raised: 
        command: StoryCollection(pathq(".").ext("story"), Engine()).one().play()
        reference: exception in on_failure
        changeable:
          - ~/((( anything )))/story.py
          - /((( anything )))/code_that_does_things.py
          - /((( anything )))/engine.py
          - <ipython-input-((( anything )))>


Exception in tear_down:
  preconditions:
    files:
      example.story: |
        Do thing:
          scenario:
            - Do thing
      engine.py: |
        from hitchstory import BaseEngine
        from code_that_does_things import *

        class Engine(BaseEngine):
            def do_thing(self):
                pass

            def tear_down(self):
                raise_example_exception()
  scenario:
    - Run command: |
        from hitchstory import StoryCollection
        from pathquery import pathq
        from engine import Engine

    - Exception raised: 
        command: StoryCollection(pathq(".").ext("story"), Engine()).one().play()
        reference: exception in tear_down
        changeable:
          - ~/((( anything )))/story.py
          - /((( anything )))/code_that_does_things.py
          - /((( anything )))/engine.py
          - <ipython-input-((( anything )))>
