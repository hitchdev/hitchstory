Shortcut lookup for story names:
  preconditions:
    example1.story: |
      Create file:
        scenario:
          - Create file
      Create file again:
        scenario:
          - Create file
    example2.story: |
      Create files:
        scenario:
          - Create file
    setup: |
      from hitchstory import StoryCollection, BaseEngine
      from code_that_does_things import *
      from pathquery import pathq


      class Engine(BaseEngine):
          def create_file(self, filename="step1.txt", content="example"):
              with open(filename, 'w') as handle:
                  handle.write(content)
  variations:
    Story not found:
      preconditions:
        code: |
          StoryCollection(pathq(".").ext("story"), Engine()).shortcut("toast").play()
      scenario:
      - Raises Exception: Story 'toast' not found.

    More than one story found:
      preconditions:
        code: |
          StoryCollection(pathq(".").ext("story"), Engine()).shortcut("file").play()
      scenario:
      - Raises Exception: |
          More than one matching story:
          Create file again (in /home/colm/.hitch/90646u/state/example1.story)
          Create files (in /home/colm/.hitch/90646u/state/example2.story)
          Create file (in /home/colm/.hitch/90646u/state/example1.story)

    Story found and run:
      preconditions:
        code: |
          results = StoryCollection(pathq(".").ext("story"), Engine()).shortcut("file", "again").play()
          output(results.report())
      scenario:
      - Run code
      - Output will be:
          reference: successful
          changeable:
          - /((( anything )))/example1.story


  #scenario:
    #- Run command: |
    #- Assert exception:
        #command: StoryCollection(pathq(".").ext("story"), Engine()).shortcut("toast").play()
        #exception: StoryNotFound

    #- Assert exception:
        #command: StoryCollection(pathq(".").ext("story"), Engine()).shortcut("file").play()
        #exception: MoreThanOneStory

    #- Run command: |
        #results = StoryCollection(pathq(".").ext("story"), Engine()).shortcut("file", "again").play()
        #output(results.report())
    #- Output will be:
        #reference: successful
        #changeable:
          #- /((( anything )))/example1.story
