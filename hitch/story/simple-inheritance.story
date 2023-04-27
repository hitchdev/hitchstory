Inherit one story from another simply:
  docs: inheritance
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

    The base story given preconditions and parameters will be
    used while the child story given preconditions will override
    them.

    The steps of the parent stories, if they have any steps,
    will be executed before the child story steps.
  given:
    files:
      example.story: |
        Login:
          about: Simple log in.
          with:
            username: AzureDiamond
            password: hunter2
          given:
            url: /loginurl
            files:
              a.txt: a
              b.txt: b
          steps:
          - Fill form:
              username: (( username ))
              password: (( password ))
          - Click: login


        Log in on another url:
          about: Alternate log in URL.
          based on: login
          given:
            url: /alternativeloginurl

        Log in as president:
          about: For stories that involve Trump.
          based on: login
          with:
            username: DonaldTrump
            password: iamsosmrt
      engine.py: |
        from hitchstory import BaseEngine, GivenDefinition, GivenProperty
        from strictyaml import Map, Int, Str, MapPattern, Optional


        class Engine(BaseEngine):
            given_definition = GivenDefinition(
                url=GivenProperty(schema=Str()),
                files=GivenProperty(
                    schema=MapPattern(Str(), Str()),
                    inherit_via=GivenProperty.REPLACE,
                ),
            )

            def set_up(self):
                print("visit {0}".format(self.given['url']))
                
                for filename, content in self.given.get("files", {}).items():
                    print("{}: {}".format(filename, content))

            def fill_form(self, **textboxes):
                for name, text in sorted(textboxes.items()):
                    print("with {0}".format(name))
                    print("enter {0}".format(text))

            def click(self, item):
                print("clicked on {0}".format(item))
    setup: |
      from engine import Engine
      from hitchstory import StoryCollection
      from pathlib import Path
      from ensure import Ensure

      collection = StoryCollection(Path(".").glob("*.story"), Engine())
  variations:
    Original story:
      steps:
      - Run:
          code: collection.named("Login").play()
          will output: |-
            RUNNING Login in /path/to/working/example.story ... visit /loginurl
            a.txt: a
            b.txt: b
            with password
            enter (( password ))
            with username
            enter (( username ))
            clicked on login
            SUCCESS in 0.1 seconds.


    Override given:
      steps:
      - Run:
          code: collection.named("Log in on another url").play()
          will output: |-
            RUNNING Log in on another url in /path/to/working/example.story ... visit /alternativeloginurl
            a.txt: a
            b.txt: b
            with password
            enter (( password ))
            with username
            enter (( username ))
            clicked on login
            SUCCESS in 0.1 seconds.


    Override parameters:
      steps:
      - Run:
          code: collection.named("Log in as president").play()
          will output: |-
            RUNNING Log in as president in /path/to/working/example.story ... visit /loginurl
            a.txt: a
            b.txt: b
            with password
            enter (( password ))
            with username
            enter (( username ))
            clicked on login
            SUCCESS in 0.1 seconds.


    Only children:
      steps:
      - Run:
          code: |
            print('\n'.join([
                story.name for story in collection.only_uninherited().ordered_by_file()
            ]))
          will output: |-
            Log in on another url
            Log in as president
