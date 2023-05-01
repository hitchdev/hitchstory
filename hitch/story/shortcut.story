Shortcut lookup for story names:
  category: runner
  docs: shortcut-lookup
  about: |
    Hunting for and specifying particular story to run can be a pain.

    Using the 'shortcut' function you can select a specific story
    to run just by specifying one or more key words that appear in
    the story title. The case is ignored, as are special characters.

    If you specify key words that match no stories or more than one
    story, an error is raised.
  given:
    files:
      example1.story: |
        Create file:
          steps:
            - Create file
        Create file again:
          steps:
            - Create file
      example2.story: |
        Create files:
          steps:
            - Create file
    setup: |
      from hitchstory import StoryCollection, BaseEngine
      from ensure import Ensure
      from pathlib import Path

      class Engine(BaseEngine):
          def create_file(self, filename="step1.txt", content="example"):
              with open(filename, 'w') as handle:
                  handle.write(content)

      story_collection = StoryCollection(Path(".").glob("*.story"), Engine())
  variations:
    Story found and run:
      steps:
      - Run:
          code: |
            story_collection.shortcut("file", "again").play()
          will output: |-
            RUNNING Create file again in /path/to/working/example1.story ... SUCCESS in 0.1 seconds.


    Story not found:
      steps:
      - Run:
          code: story_collection.shortcut("toast").play()
          raises:
            type: hitchstory.exceptions.StoryNotFound
            message: Story 'toast' not found.

    More than one story found:
      steps:
      - Run:
          code: story_collection.shortcut("file").play()
          raises:
            type: hitchstory.exceptions.MoreThanOneStory
            message: |-
              More than one matching story:
              Create file (in /path/to/working/example1.story)
              Create file again (in /path/to/working/example1.story)
              Create files (in /path/to/working/example2.story)
