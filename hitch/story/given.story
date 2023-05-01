Given preconditions:
  docs: engine/given
  about: |
    All hitch stories are comprised of preconditions followed by steps.

    Hitchstory lets you define preconditions using the `given:` keyword
    in YAML and then refer to these preconditions in the `set_up` method
    or steps using `self.given['property name']`.

    The given property names need to first be specified in the engine
    using GivenDefinition and GivenProperty.
    
    The schemas are specified using [StrictYAML validators](../../../../strictyaml/using).

    The following example shows a browser precondition being used to set up
    a mock selenium object for a test that uses a browser.
  given:
    files:
      example.story: |
        Load with chrome:
          given:
            browser configuration:
              name: chrome
              version: 22.0
              platform: linux
          steps:
          - Load website

        Load with small firefox window:
          given:
            browser configuration:
              name: firefox
              platform: linux
              dimensions:
                height: 200
                width: 200
          steps:
          - Load website
      engine.py: |
        from hitchstory import BaseEngine, GivenDefinition, GivenProperty
        from strictyaml import Optional, Str, Map, Enum, Seq, Int, MapPattern
        from mockselenium import Webdriver

        class Engine(BaseEngine):
            given_definition=GivenDefinition(
                browser_configuration=GivenProperty(
                    schema=Map(
                        {
                            "name": Str(),
                            "platform": Enum(["linux", "osx", "windows"]),
                            Optional("version"): Str(),
                            Optional("dimensions"): Map({"height": Int(), "width": Int()}),
                        }
                    ),
                    inherit_via=GivenProperty.OVERRIDE,
                )
            )

            def set_up(self):
                browser = self.given["browser configuration"]
                self.driver = Webdriver(
                    name=browser['name'],
                    platform=browser['platform'],
                    version=browser.get('version'),
                    dimensions=browser.get('dimensions', {"height": 1000, "width": 1000}),
                )

            def load_website(self):
                self.driver.visit("http://www.google.com")
    setup: |
      from hitchstory import StoryCollection
      from pathlib import Path
      from engine import Engine
  variations:
    Specified:
      steps:
      - Run:
          code: |
            StoryCollection(Path(".").glob("*.story"), Engine()).ordered_by_name().play()
          will output: |-
            RUNNING Load with chrome in /path/to/working/example.story ...
            Browser name: chrome
            Platform: linux
            Version: 22.0
            Dimensions: 1000 x 1000

            Visiting http://www.google.com
            SUCCESS in 0.1 seconds.
            RUNNING Load with small firefox window in /path/to/working/example.story ...
            Browser name: firefox
            Platform: linux
            Dimensions: 200 x 200

            Visiting http://www.google.com
            SUCCESS in 0.1 seconds.
