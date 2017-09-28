Story with parameters:
  description: |
    Parameterized stories are used to describe stories
    which are essentially the same except for one or more
    things which change.

    A good example is a story for a user to log in with
    a browser which may be done with a number of different
    browsers - the parameter.

    Parameters can be used in preconditions and in steps.
  preconditions:
    example.story: |
      Click magic button:
        default:
          browser:
            name: firefox
            version: 37
        preconditions:
          browser: (( browser ))
        scenario:
          - Click on button
          - Save screenshot:
              browser: (( browser ))
    engine.py: "from hitchstory import BaseEngine, StorySchema, validate\nfrom strictyaml\
      \ import Map, Seq, Int, Str, Optional\nfrom code_that_does_things import *\n\
      \nclass Engine(BaseEngine):\n    schema = StorySchema(\n        preconditions={\n\
      \            Optional(\"browser\"): Map({\"name\": Str(), \"version\": Int()}),\n\
      \        },\n    )\n    \n    def set_up(self):\n        append(self.preconditions['browser']['name'])\n\
      \        append(self.preconditions['browser']['version'])\n\n    def click_on_button(self):\n\
      \        append(\"clicked!\")\n    \n    @validate(browser=Map({\"name\": Str(),\
      \ \"version\": Int()}))\n    def save_screenshot(self, browser):\n        append('save\
      \ screenshot:')\n        append(\"screenshot-{0}-{1}.png\".format(browser['name'],\
      \ browser['version']))\n"
    setup: |
      from hitchstory import StoryCollection
      from pathquery import pathq
      from engine import Engine
    code: |
      print(StoryCollection(pathq(".").ext("story"), Engine()).one().play().report())

  variations:
    Default:
      scenario:
      - Run code
      - Output is: |
          firefox
          37
          clicked!
          save screenshot:
          screenshot-firefox-37.png

    Specify parameters with code:
      preconditions:
        code: |
          storybook = StoryCollection(pathq(".").ext("story"), Engine())

          print(storybook.with_params(browser={"name": "ie", "version": "6"}).one().play().report())
      scenario:
      - Run code
      - Output is: |
          ie
          6
          clicked!
          save screenshot:
          screenshot-ie-6.png
