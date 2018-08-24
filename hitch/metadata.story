Extra story metadata - e.g. adding JIRA ticket numbers to stories:
  docs: metadata
  about: |
    Stories do not exist in a vaccuum. Each and every story is
    related to issues on issue trackers, specialist documentation,
    people, external resources and much more.

    The best place to document this additional metadata is within
    the story itself. You can thus define additional YAML metadata
    to be included alongside the story.

    What kind of metadata you add to stories is up to you -
    simply add the names of the properties you want to add
    in the info parameter of your engine InfoDefinition and
    specify the structure of the metadata using StrictYAML
    validators inside the InfoProperty object.

    This example shows how you can add a series of JIRA tickets
    and feature names as metadata on a story.

    It also demonstrates code that will filter stories to play
    by jira ticket.
  given:
    example.story: |
      Build city:
        about: Build a great city. The best.
        jiras: JIRA-123, JIRA-124
        features: files, creating
        steps:
        - Reticulate splines

      Live in city:
        jiras: JIRA-789
        features: other
        steps:
        - Kick llama's ass

        variations:
          Build llama zoo:
            jiras: JIRA-123
            features: zoo
            steps:
            - Kick llama's ass
    setup: |
      from hitchstory import StoryCollection, BaseEngine, InfoDefinition, InfoProperty
      from strictyaml import Map, Str, CommaSeparated, Optional
      from pathquery import pathq
      from ensure import Ensure
      from code_that_does_things import reticulate_splines, kick_llamas_ass

      class Engine(BaseEngine):
          info_definition=InfoDefinition(
              jiras=InfoProperty(schema=CommaSeparated(Str())),
              features=InfoProperty(schema=CommaSeparated(Str())),
          )

          def reticulate_splines(self):
              print('reticulate splines')

          def kick_llamas_ass(self):
              print('kick llamas ass')

      story_collection = StoryCollection(pathq(".").ext("story"), Engine())
  variations:
    Run all stories:
      steps:
      - Run:
          code: story_collection.ordered_by_name().play()
          will output: |-
            RUNNING Build city in /path/to/example.story ... reticulate splines
            SUCCESS in 0.1 seconds.
            RUNNING Live in city in /path/to/example.story ... kick llamas ass
            SUCCESS in 0.1 seconds.
            RUNNING Live in city/Build llama zoo in /path/to/example.story ... kick llamas ass
            kick llamas ass
            SUCCESS in 0.1 seconds.


    Run only filtered stories:
      steps:
      - Run:
          code: |
            story_collection.filter(lambda story: "JIRA-124" in story.info['jiras']).ordered_by_name().play()
          will output: |-
            RUNNING Build city in /path/to/example.story ... reticulate splines
            SUCCESS in 0.1 seconds.


    Info:
      steps:
      - Run: |
          Ensure([story.info['jiras'] for story in story_collection.ordered_by_name()]).equals(
              [["JIRA-123", "JIRA-124"], ["JIRA-789", ], ["JIRA-123"]]
          )
