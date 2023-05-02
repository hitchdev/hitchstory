Story inheritance - steps:
  docs: inheritance/steps
  about: |
    Child stories that inherit from parent stories can have:
    
    * `following steps:`
    * `replacement steps:`
    * `steps:` (if the parent story has no steps of its own)
    
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

        Visit inbox:
          about: uses parent login and following steps.
          based on: login
          following steps:
          - Click: inbox

        Login as hiya and visit inbox:
          about: uses parent properties but replaces its own steps.
          based on: login
          replacement steps:
          - Fill form:
              username: hiya
              password: password
          - Click: login
          - Click: inbox

        Login as hiya and visit different pages:
          about: login as hiya and visit inbox
          based on: Login as hiya and visit inbox
          variations:
            Dashboard:
              replacement steps:
              - Fill form:
                  username: hiya
                  password: password
              - Click: login
              - Click: dashboard
          

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

    With following steps:
      steps:
      - Run:
          code: collection.named("Visit inbox").play()
          will output: |-
            RUNNING Visit inbox in /path/to/working/example.story ... use browser firefox
            visit /loginurl
            with password
            enter password
            with username
            enter hello
            clicked on login
            clicked on inbox
            SUCCESS in 0.1 seconds.

    With replacement steps:
      steps:
      - Run:
          code: collection.named("Login as hiya and visit inbox").play()
          will output: |-
            RUNNING Login as hiya and visit inbox in /path/to/working/example.story ... use browser firefox
            visit /loginurl
            with password
            enter password
            with username
            enter hiya
            clicked on login
            clicked on inbox
            SUCCESS in 0.1 seconds.

    With variations and replacement steps:
      steps:
      - Run:
          code: collection.named("Login as hiya and visit different pages/Dashboard").play()
          will output: |-
            RUNNING Login as hiya and visit different pages/Dashboard in /path/to/working/example.story ... use browser firefox
            visit /loginurl
            with password
            enter password
            with username
            enter hiya
            clicked on login
            clicked on dashboard
            SUCCESS in 0.1 seconds.
