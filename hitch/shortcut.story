Shortcut lookup for story names:
  preconditions:
    files:
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
  scenario:
    - Run command: |
        from hitchstory import StoryCollection, BaseEngine
        from pathquery import pathq


        class Engine(BaseEngine):
            def create_file(self, filename="step1.txt", content="example"):
                with open(filename, 'w') as handle:
                    handle.write(content)

    - Assert exception:
        command: StoryCollection(pathq(".").ext("story"), Engine()).shortcut("toast").play()
        exception: StoryNotFound

    - Assert exception:
        command: StoryCollection(pathq(".").ext("story"), Engine()).shortcut("file").play()
        exception: MoreThanOneStory

    - Run command: |
        results = StoryCollection(pathq(".").ext("story"), Engine()).shortcut("file", "again").play()
        output(results.report())
    - Output will be:
        reference: successful
        changeable:
          - /((( anything )))/example1.story
