Variations:
  docs: variations
  about: |
    Some stories are very similar except for a few changed items. You
    can create substories within the same story in order to enumerate
    all of the possible permutations of preconditions and steps
    under a particular story.

    Variations are simply inherited stories defined on the same story.
  given:
    core files:
      example.story: |
        Create files:
          given:
            content: dog
            hierarchical content:
              x: 1
              y:
                - 42
          steps:
            - Do thing with precondition
            - Do other thing: dog
            - Do yet another thing
            - Do a fourth thing:
                animals:
                  pond animal: frog
          variations:
            cat:
              about: create a cat file
              given:
                content: cat
    setup: |
      from hitchstory import StoryCollection, BaseEngine, GivenDefinition, GivenProperty, validate
      from strictyaml import Map, Seq, Int, Str, Optional
      from pathquery import pathquery
      from ensure import Ensure
      from path import Path


      class Engine(BaseEngine):
          given_definition=GivenDefinition(
              content=GivenProperty(schema=Str()),
              hierarchical_content=GivenProperty(
                  schema=Map({"x": Int(), "y": Seq(Str())})
              ),
          )

          def do_other_thing(self, parameter):
              assert type(parameter) is str
              print(parameter)

          def do_thing_with_precondition(self):
              assert type(self.given['content']) is str
              print(self.given['content'])

          def do_yet_another_thing(self):
              assert type(self.given['hierarchical_content']['y'][0]) is str
              print(self.given['hierarchical_content']['y'][0])

          @validate(animals=Map({"pond animal": Str()}))
          def do_a_fourth_thing(self, animals=None):
              assert type(animals['pond animal']) is str
              print(animals['pond animal'])

      story_collection = StoryCollection(pathquery(".").ext("story"), Engine())
  variations:
    Play:
      steps:
      - Run:
          code: |
            story_collection.shortcut("cat").play().report()
          will output: |-
            RUNNING Create files/cat in /path/to/working/example.story ... cat
            dog
            42
            frog
            SUCCESS in 0.1 seconds.

    Non-variations can be selected from the collection:
      steps:
      - Run:
          code: |
            Ensure([
                story.name for story in story_collection.non_variations().ordered_by_name()
            ]).equals(
                ["Create files", ]
            )

    Variations can be grabbed directly from a story object:
      steps:
      - Run:
          code: |
            Ensure([
                story.name for story in story_collection.named("Create files").variations
            ]).equals(
                ["Create files/cat"],
            )

    Only child stories can be selected also:
      steps:
      - Run:
          code: |
            Ensure([
                story.name for story in story_collection.only_uninherited().ordered_by_name()
            ]).equals(
                ["Create files/cat"],
            )

    Generate documentation:
      given:
        files:
          docstory.yml: |
            story: |
              # {{ name }}
              
              {% for variation in variations %}
              {{ variation.documentation() }}
              {% endfor %}
            given:
              content: '{{ content }}'
              hierarchical_content: '{{ hierarchical_content["x"] }}'
            variation: |
              ## {{ name }}
              ## {{ full_name }}
              
              {{ about }}
              
              {% for name, property in given.child.items() %}
              {{ property.documentation() }}
              {% endfor %}
      steps:
      - Run:
          code: |
            print(
                story_collection.with_documentation(
                    Path("docstory.yml").text()
                ).named("Create files").documentation()
            )
          will output: |-
            # Create files


            ## cat
            ## Create files/cat

            create a cat file


            cat
