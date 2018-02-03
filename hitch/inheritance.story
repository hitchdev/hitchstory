Inherit one story from another:
  about: |
    You can break most software down into a series of
    individual linear behavioral stories.
    
    However, software stories naturally branch. In order to
    send an email or delete an email you must first always log
    in.

    While it would be possible to write out each individual
    story for every possible branch, this would result in a
    story suite that is WET instead of DRY and that creates
    a maintenance headache.

    Story inheritance allows you to base stories on other stories.
    The base story preconditions will all be used while the
    child story preconditions (if it has any) will override
    them.

    The same is so for story parameters.

    The base story scenario will always be executed before
    continuing with the child story scenario, however,
    if you do not want that you do not have to give the base
    story any steps to execute.
  given:
    example.story: |
      Login:
        with:
          username: AzureDiamond
          password: hunter2
        given:
          url: /loginurl
        steps:
        - Fill form:
            username: (( username ))
            password: (( password ))
        - Click: login
      
      
      Log in on another url:
        based on: login
        given:
          url: /alternativeloginurl
      
      Log in as president:
        based on: login
        with:
          username: DonaldTrump
          password: iamsosmrt
    engine.py: |
      from hitchstory import BaseEngine, GivenDefinition, GivenProperty
      from strictyaml import Map, Int, Str, Optional
      from code_that_does_things import append


      class Engine(BaseEngine):
          given_definition = GivenDefinition(
              url=GivenProperty(schema=Str()),
          )

          def set_up(self):
              append("visit {0}".format(self.given.url))

          def fill_form(self, **textboxes):
              for name, text in sorted(textboxes.items()):
                  append("with {0}".format(name))
                  append("enter {0}".format(text))
          
          def click(self, item):
              append("clicked on {0}".format(item))
    setup: |
      from engine import Engine
      from hitchstory import StoryCollection
      from pathquery import pathq
      from ensure import Ensure

      collection = StoryCollection(pathq(".").ext("story"), Engine())
  variations:
    Original story:
      steps:
      - Run:
          code: collection.named("Login").play()
      - Output is: |
          visit /loginurl
          with password
          enter hunter2
          with username
          enter AzureDiamond
          clicked on login


    Override given:
      steps:
      - Run:
          code: collection.named("Log in on another url").play()
      - Output is: |
          visit /alternativeloginurl
          with password
          enter hunter2
          with username
          enter AzureDiamond
          clicked on login

    Override parameters:
      steps:
      - Run:
          code: collection.named("Log in as president").play()
      - Output is: |
          visit /loginurl
          with password
          enter iamsosmrt
          with username
          enter DonaldTrump
          clicked on login


    Only children:
      steps:
      - Run:
          code: |
            Ensure([
                story.name for story in collection.only_uninherited().ordered_by_file()
            ]).equals(
                ["Log in on another url", "Log in as president"],
            )


Attempt inheritance from non-existent story:
  given:
    example.story: |
      Write to file:
        based on: Create files
        steps:
          - Do thing two
    setup: |
      from hitchstory import StoryCollection, BaseEngine
      from code_that_does_things import output
      from strictyaml import Map, Str
      from pathquery import pathq


      class Engine(BaseEngine):
          def do_thing_one(self):
              output("thing one")

          def do_thing_two(self):
              output("thing two")

  steps:
  - Run:
      code: StoryCollection(pathq(".").ext("story"), Engine()).named("Write to file").play()
      raises:
        type: hitchstory.exceptions.BasedOnStoryNotFound
        message: Story 'Create files' which 'Write to file' in '/path/to/example.story'
          is based upon not found.
