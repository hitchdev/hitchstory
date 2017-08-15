Multiple stories played:
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
        command: StoryCollection(pathq(".").ext("story"), Engine()).one()
        exception: Create file again

    - Run command: |
        results = StoryCollection(pathq(".").ext("story"), Engine()).ordered_by_name().play()
        output(results.report())
    - Output is: |
        STORY RAN SUCCESSFULLY ((( anything )))/example1.story: Create file in 0.1 seconds.
        STORY RAN SUCCESSFULLY ((( anything )))/example1.story: Create file again in 0.1 seconds.
        STORY RAN SUCCESSFULLY ((( anything )))/example2.story: Create files in 0.1 seconds.


Multiple stories played in a filename:
  preconditions:
    files:
      base.story: |
        Base story:
          preconditions:
            run: yes
      example1.story: |
        Create file:
          based on: Base story
          scenario:
            - Create file
        Create file again:
          based on: Base story
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

    - Run command: |
        results = StoryCollection(pathq(".").ext("story"), Engine()).in_filename("example1.story").ordered_by_name().play()
        output(results.report())
    - Output is: |
        STORY RAN SUCCESSFULLY ((( anything )))/example1.story: Create file in 0.1 seconds.
        STORY RAN SUCCESSFULLY ((( anything )))/example1.story: Create file again in 0.1 seconds.


Continue on failure and stop on failure:
  preconditions:
    files:
      example1.story: |
        A Create file:
          scenario:
            - Create file
        B Create file:
          scenario:
            - Fail
      example2.story: |
        C Create file a third time:
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

            def fail(self):
                raise Exception("Error")

    - Run command: |
        results = StoryCollection(
            pathq(".").ext("story"), Engine()
        ).ordered_by_name().continue_on_failure().play()
        output(results.report())
    - Output will be:
        reference: continue-on-failure
        changeable:
          - STORY RAN SUCCESSFULLY ((( anything )))/example1.story
          - FAILURE IN ((( anything )))/example1.story
          - ((( anything )))/story.py
          - ((( anything )))/engine.py
          - STORY RAN SUCCESSFULLY ((( anything )))/example2.story

    - Run command: |
        results = StoryCollection(
            pathq(".").ext("story"), Engine()
        ).ordered_by_name().play()
        output(results.report())
    - Output will be:
        reference: stop-on-failure
        changeable:
          - STORY RAN SUCCESSFULLY ((( anything )))/example1.story
          - FAILURE IN ((( anything )))/example1.story
          - ((( anything )))/story.py
          - ((( anything )))/engine.py
