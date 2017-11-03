Story with parameters:
  description: |
    Parameterized stories are used to describe stories
    which are essentially the same except for one or more
    things which change.

    A good example is a story for a user to log in with
    a browser which may be done with a number of different
    browsers - the parameter.

    Parameters can be used in preconditions and in steps.
  given:
    example.story: |
      Click magic button:
        with:
          browser:
            name: firefox
            version: 37
        given:
          browser: (( browser ))
        steps:
        - Click on button
        - Save screenshot:
            browser: (( browser ))

        variations:
          with chrome:
            with:
              browser:
                name: chrome
                version: 153
    engine.py: |
      from hitchstory import BaseEngine, StorySchema, validate
      from strictyaml import Map, Seq, Int, Str, Optional
      from code_that_does_things import *

      class Engine(BaseEngine):
          schema=StorySchema(
              given={
                  Optional("browser"): Map({"name": Str(), "version": Int()}),
              },
          )

          def set_up(self):
              append(self.given['browser']['name'])
              append(self.given['browser']['version'])

          def click_on_button(self):
              append("clicked!")

          @validate(browser=Map({"name": Str(), "version": Int()}))
          def save_screenshot(self, browser):
              append('save screenshot:')
              append("screenshot-{0}-{1}.png".format(browser['name'], browser['version']))
    setup: |
      from hitchstory import StoryCollection
      from pathquery import pathq
      from engine import Engine
  variations:
    Default:
      steps:
      - Run:
          code: |
            print(StoryCollection(pathq(".").ext("story"), Engine()).named("Click magic button").play().report())
      - Output is: |
          firefox
          37
          clicked!
          save screenshot:
          screenshot-firefox-37.png

    Variation:
      steps:
      - Run:
          code: |
            print(StoryCollection(pathq(".").ext("story"), Engine()).named("Click magic button/with chrome").play().report())
      - Output is: |
          chrome
          153
          clicked!
          save screenshot:
          screenshot-chrome-153.png

    Specify parameters with code:
      steps:
      - Run:
          code: |
            storybook = StoryCollection(pathq(".").ext("story"), Engine())

            print(storybook.with_params(browser={"name": "ie", "version": "6"}).named("Click magic button").play().report())
      - Output is: |
          ie
          6
          clicked!
          save screenshot:
          screenshot-ie-6.png
