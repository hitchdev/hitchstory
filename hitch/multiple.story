Multiple stories played:
  about: |
    Running multiple stories in sequence is necessary when
    you want to do a regression sweep to make sure nothing
    has broken.
    
    By default hitchstory will stop when it sees its first
    failure. This behavior can be changed though.
  given:
    base.story: |
      Base story:
        given:
          random variable: some value
    example1.story: |
      Create file:
        based on: base story
        steps:
          - Create file
      Create file again:
        based on: base story
        steps:
          - Create file
    example2.story: |
      Create files:
        based on: base story
        steps:
          - Create file
    setup: |
      from hitchstory import StoryCollection, BaseEngine, GivenDefinition, GivenProperty
      from pathquery import pathq
      from ensure import Ensure

      class Engine(BaseEngine):
          given_definition=GivenDefinition(
              random_variable=GivenProperty()
          )
      
          def create_file(self, filename="step1.txt", content="example"):
              with open(filename, 'w') as handle:
                  handle.write(content)
  variations:
    Running all stories in file order:
      steps:
      - Run:
          code: |
            results = StoryCollection(
                [
                    "base.story",
                    "example1.story",
                    "example2.story",
                ],
                Engine()
            ).ordered_by_file().play()
            Ensure(results.all_passed).is_true()
          will output: |-
            RUNNING Base story in /path/to/base.story ... SUCCESS in 0.1 seconds.
            RUNNING Create file in /path/to/example1.story ... SUCCESS in 0.1 seconds.
            RUNNING Create file again in /path/to/example1.story ... SUCCESS in 0.1 seconds.
            RUNNING Create files in /path/to/example2.story ... SUCCESS in 0.1 seconds.

    Running all tests ordered by name in 'example1.story':
      steps:
      - Run:
          code: |
            StoryCollection(
                pathq(".").ext("story"), Engine()
            ).in_filename("example1.story").ordered_by_name().play()
          will output: |-
            RUNNING Create file in /path/to/example1.story ... SUCCESS in 0.1 seconds.
            RUNNING Create file again in /path/to/example1.story ... SUCCESS in 0.1 seconds.


    Using .one() on a group of stories will fail:
      steps:
      - Run:
          code: |
            StoryCollection(pathq(".").ext("story"), Engine()).one()
          raises:
            type: hitchstory.exceptions.MoreThanOneStory
            message: "More than one matching story:\nBase story (in /path/to/base.story)\n\
              Create file (in /path/to/example1.story)\nCreate file again (in /path/to/example1.story)\n\
              Create files (in /path/to/example2.story)"
Fail fast:
  given:
    example1.story: |
      A Create file:
        steps:
        - Create file
      B Create file:
        steps:
        - Fail
    example2.story: |
      C Create file a third time:
        steps:
          - Create file
    setup: |
      from hitchstory import StoryCollection, BaseEngine
      from pathquery import pathq


      class Engine(BaseEngine):
          def create_file(self, filename="step1.txt", content="example"):
              with open(filename, 'w') as handle:
                  handle.write(content)

          def fail(self):
              raise Exception("Error")

  variations:
    Stop on failure is default behavior:
      steps:
      - Run:
          code: |
            StoryCollection(
                pathq(".").ext("story"), Engine()
            ).ordered_by_name().play()
          will output: |-
            RUNNING A Create file in /path/to/example1.story ... SUCCESS in 0.1 seconds.
            RUNNING B Create file in /path/to/example1.story ... FAILED in 0.1 seconds.

                B Create file:
                  steps:
                  - Fail


            [1]: function 'fail'
              examplepythoncode.py


                    59 :
                    60 :             def fail(self):
                --> 61 :                 raise Exception("Error")
                    62 :



            builtins.Exception
              Common base class for all non-exit exceptions.
            Error


    Continue on failure:
      steps:
      - Run:
          code: |
            StoryCollection(
                pathq(".").ext("story"), Engine()
            ).ordered_by_name().continue_on_failure().play()
          will output: |-
            RUNNING A Create file in /path/to/example1.story ... SUCCESS in 0.1 seconds.
            RUNNING B Create file in /path/to/example1.story ... FAILED in 0.1 seconds.

                B Create file:
                  steps:
                  - Fail


            [1]: function 'fail'
              examplepythoncode.py


                    59 :
                    60 :             def fail(self):
                --> 61 :                 raise Exception("Error")
                    62 :



            builtins.Exception
              Common base class for all non-exit exceptions.
            Error
            RUNNING C Create file a third time in /path/to/example2.story ... SUCCESS in 0.1 seconds.
