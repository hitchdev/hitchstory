Extra story metadata:
  description: |
    Stories do not exist in a vaccuum. Each and every story is
    related to other stories, issues on issue trackers,
    specialist documentation and much more. The best place
    to document this additional information and relationships is
    within the story itself.

    What kind of metadata you add to stories is up to you -
    simply add the names of the properties you want to add
    in the info parameter of your engine InfoDefinition and
    specify the structure of the metadata using StrictYAML
    validators inside the InfoProperty object.
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
              reticulate_splines()

          def kick_llamas_ass(self):
              kick_llamas_ass()

      story_collection = StoryCollection(pathq(".").ext("story"), Engine())
  variations:
    Run all stories:
      steps:
      - Run:
          code: story_collection.ordered_by_name().play()
      - Splines reticulated
      - Llama's ass kicked

    Run only filtered stories:
      steps:
      - Run:
          code: |
            story_collection.filter(lambda story: "JIRA-124" in story.info.jiras).ordered_by_name().play()
      - Splines reticulated

    Info:
      steps:
      - Run:
          code: |
            Ensure([story.info.jiras for story in story_collection.ordered_by_name()]).equals(
                [["JIRA-123", "JIRA-124"], ["JIRA-789", ], ["JIRA-123"]]
            )
