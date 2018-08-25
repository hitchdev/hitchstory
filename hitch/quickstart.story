Quickstart:
  given:
    example.story: |
      Log in:
        given:
          website: /login                  # preconditions
        steps:
          - Fill form:
              username: AzureDiamond       # parameterized steps
              password: hunter2
          - Click: login


      Send email:
        about: Core functionality of app.
        based on: log in                 # inherits from and continues from test above
        steps:
          - Click: new email
          - Fill form:
              to: Cthon98@aol.com
              contents: |                # long form text
                Hey guys,

                I think I got hacked!
          - Click: send email
          - Email was sent

    engine.py: |
      from hitchstory import BaseEngine, GivenDefinition, GivenProperty
      from mockemailchecker import email_was_sent
      from mockselenium import Webdriver
      from strictyaml import Str

      class Engine(BaseEngine):
          given_definition = GivenDefinition(
              website=GivenProperty(Str()),
          )

          def set_up(self):
              self.driver = Webdriver()
              self.driver.visit(
                  "http://localhost:5000{0}".format(self.given['website'])
              )

          def fill_form(self, **textboxes):
              for name, contents in sorted(textboxes.items()):
                  self.driver.fill_form(name, contents)

          def click(self, name):
              self.driver.click(name)

          def email_was_sent(self):
              email_was_sent()

  steps:
  - Run:
      code: |
        from hitchstory import StoryCollection
        from pathquery import pathquery
        from engine import Engine

        StoryCollection(pathquery(".").ext("story"), Engine()).named("Send email").play()
      will output: |-
        RUNNING Send email in /path/to/example.story ...
        Visiting http://localhost:5000/login
        Entering text hunter2 in password
        Entering text AzureDiamond in username
        Clicking on login
        Clicking on new email
        In contents entering text:
        Hey guys,

        I think I got hacked!


        Entering text Cthon98@aol.com in to
        Clicking on send email
        Email was sent
        SUCCESS in 0.1 seconds.
