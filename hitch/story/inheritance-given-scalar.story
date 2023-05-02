Story inheritance - override given scalar preconditions:
  docs: inheritance/override-given-scalar
  about: |
    Child stories can be based upon parent stories.

    If you change one precondition in a child story,
    when it is run the steps and the other preconditions
    will all remain the same.
    
    In the following example the given url is changed from
    /loginurl to /alternativeloginurl and the browser
    remains as firefox.
  given:
    files:
      example.story: |
        Login:
          given:
            url: /loginurl
            browser: firefox
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
                browser=GivenProperty(schema=Str()),
            )

            def set_up(self):
                print("use browser {0}".format(self.given["browser"]))
                print("visit {0}".format(self.given['url']))

            def fill_form(self, **textboxes):
                for name, text in sorted(textboxes.items()):
                    print("with {0}".format(name))
                    print("enter {0}".format(text))

            def click(self, item):
                print("clicked on {0}".format(item))
    setup: |
      from hitchstory import StoryCollection
      from engine import Engine
      from pathlib import Path

      collection = StoryCollection(Path(".").glob("*.story"), Engine())
  variations:
    Parent:
      steps:
      - Run:
          code: collection.named("Login").play()
          will output: |-
            RUNNING Login in /path/to/working/example.story ... use browser firefox
            visit /loginurl
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
            RUNNING Login in /path/to/working/example.story ... use browser firefox
            visit /loginurl
            with password
            enter password
            with username
            enter hello
            clicked on login
            SUCCESS in 0.1 seconds.
