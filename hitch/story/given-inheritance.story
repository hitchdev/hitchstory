Given preconditions - simple override via inheritance:
  about: |
    Hitch stories can inherit steps and given preconditions.
  given:
    core files:
      example.story: |
        Login:
          given:
            url: /loginurl
          steps:
          - Fill form:
              username: hello
              password: password
          - Click: login


        Log in on alternate url:
          based on: login
          given:
            url: /alternativeloginurl

      engine.py: |
        from hitchstory import BaseEngine, GivenDefinition, GivenProperty
        from strictyaml import Map, Int, Str, MapPattern, Optional


        class Engine(BaseEngine):
            given_definition = GivenDefinition(
                url=GivenProperty(schema=Str()),
            )

            def set_up(self):
                print("visit {0}".format(self.given['url']))

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
    Parent:
      steps:
      - Run:
          code: collection.named("Login").play()
          will output: |-
            RUNNING Login in /path/to/working/example.story ... visit /loginurl
            with password
            enter password
            with username
            enter hello
            clicked on login
            SUCCESS in 0.1 seconds.
            
    Child:
      steps:
      - Run:
          code: collection.named("Login").play()
          will output: |-
            RUNNING Login in /path/to/working/example.story ... visit /loginurl
            with password
            enter password
            with username
            enter hello
            clicked on login
            SUCCESS in 0.1 seconds.
