Multiple stories played:
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
      from hitchstory import StoryCollection, BaseEngine
      from pathquery import pathq
      from ensure import Ensure

      class Engine(BaseEngine):
          def create_file(self, filename="step1.txt", content="example"):
              with open(filename, 'w') as handle:
                  handle.write(content)
  variations:
    Running all tests in order of name:
      steps:
      - Run:
          code: |
            results = StoryCollection(pathq(".").ext("story"), Engine()).ordered_by_name().play()
            Ensure(results.all_passed).is_true()
            print(results.report())
          will output: |-
            STORY RAN SUCCESSFULLY /path/to/base.story: Base story in 0.1 seconds.
            STORY RAN SUCCESSFULLY /path/to/example1.story: Create file in 0.1 seconds.
            STORY RAN SUCCESSFULLY /path/to/example1.story: Create file again in 0.1 seconds.
            STORY RAN SUCCESSFULLY /path/to/example2.story: Create files in 0.1 seconds.

    Running all tests in a single file:
      steps:
      - Run:
          code: |
            results = StoryCollection(pathq(".").ext("story"), Engine()).in_filename("example1.story").ordered_by_name().play()
            print(results.report())
          will output: |-
            STORY RAN SUCCESSFULLY /path/to/example1.story: Create file in 0.1 seconds.
            STORY RAN SUCCESSFULLY /path/to/example1.story: Create file again in 0.1 seconds.


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
            results = StoryCollection(
                pathq(".").ext("story"), Engine()
            ).ordered_by_name().play()
            print(results.report())
          will output: |-
            "B Create file" in 0.1 seconds.


                B Create file:
                  steps:
                  - Fail



            [2]: function 'fail'
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
            results = StoryCollection(
                pathq(".").ext("story"), Engine()
            ).ordered_by_name().continue_on_failure().play()
            print(results.report())
          will output: |-
            B Create file:
                  steps:
                  - Fail



            [2]: function 'fail'
              examplepythoncode.py


                    59 :
                    60 :             def fail(self):
                --> 61 :                 raise Exception("Error")
                    62 :



            builtins.Exception
              Common base class for all non-exit exceptions.
            Error
            STORY RAN SUCCESSFULLY /path/to/example2.story: C Create file a third time in 0.1 seconds.
