Quickstart:
  given:
    files:
      example.story: |
        Logged in:
          given:
            website: /login  # preconditions
          steps:
          - Form filled:
              username: AzureDiamond
              password: hunter2
          - Clicked: login


        Email sent:
          about: |
            The most basic email with no subject, cc or bcc
            set.
          based on: logged in             # inherits from and continues from test above
          following steps:
          - Clicked: new email
          - Form filled:
              to: Cthon98@aol.com
              contents: |                # long form text
                Hey guys,

                I think I got hacked!
          - Clicked: send email
          - Email was sent

      engine.py: |
        from hitchstory import BaseEngine, GivenDefinition, GivenProperty
        from hitchstory import Failure, strings_match
        from mockemailchecker import email_was_sent
        from mockselenium import Webdriver
        from strictyaml import Str

        class Engine(BaseEngine):
            given_definition = GivenDefinition(
                website=GivenProperty(Str()),
            )
            
            def __init__(self, rewrite=False):
                self._rewrite = rewrite

            def set_up(self):
                self.driver = Webdriver()
                self.driver.visit(
                    "http://localhost:5000{0}".format(self.given['website'])
                )

            def form_filled(self, **textboxes):
                for name, contents in sorted(textboxes.items()):
                    self.driver.fill_form(name, contents)

            def clicked(self, name):
                self.driver.click(name)
            
            def failing_step(self):
                raise Failure("This was not supposed to happen")
            
            def error_message_displayed(self, expected_message):
                """Demonstrates steps that can rewrite themselves."""
                actual_message = "error message!"
                try:
                    strings_match(expected_message, actual_message)
                except Failure:
                    self.current_step.rewrite("expected_message").to(actual_message)

            def email_was_sent(self):
                email_was_sent()

  steps:
  - Run:
      code: |
        from hitchstory import StoryCollection
        from pathlib import Path
        from engine import Engine

        StoryCollection(Path(".").glob("*.story"), Engine()).named("Email sent").play()
      will output: |-
        RUNNING Email sent in /path/to/working/example.story ...
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
