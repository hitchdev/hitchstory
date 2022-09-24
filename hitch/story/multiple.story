Play multiple stories in sequence:
  docs: play-multiple-stories
  about: |
    Running multiple stories in sequence is necessary when
    you want to do a regression sweep to make sure nothing
    has broken.

    By default hitchstory will stop when it sees its first
    failure. This behavior can be changed though.
  given:
    files:
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
      from pathquery import pathquery
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
            RUNNING Base story in /path/to/working/base.story ... SUCCESS in 0.1 seconds.
            RUNNING Create file in /path/to/working/example1.story ... SUCCESS in 0.1 seconds.
            RUNNING Create file again in /path/to/working/example1.story ... SUCCESS in 0.1 seconds.
            RUNNING Create files in /path/to/working/example2.story ... SUCCESS in 0.1 seconds.

    Running all tests ordered by name in 'example1.story':
      steps:
      - Run:
          code: |
            StoryCollection(
                pathquery(".").ext("story"), Engine()
            ).in_filename("example1.story").ordered_by_name().play()
          will output: |-
            RUNNING Create file in /path/to/working/example1.story ... SUCCESS in 0.1 seconds.
            RUNNING Create file again in /path/to/working/example1.story ... SUCCESS in 0.1 seconds.


    Using .one() on a group of stories will fail:
      steps:
      - Run:
          code: |
            StoryCollection(pathquery(".").ext("story"), Engine()).one()
          raises:
            type: hitchstory.exceptions.MoreThanOneStory
            message: |-
              More than one matching story:
              Base story (in /path/to/working/base.story)
              Create file (in /path/to/working/example1.story)
              Create file again (in /path/to/working/example1.story)
              Create files (in /path/to/working/example2.story)
