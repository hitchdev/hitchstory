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
        from strictyaml import Str

        class Engine(BaseEngine):
            given_definition = GivenDefinition(
                website=GivenProperty(Str()),
            )
            
            def __init__(self, rewrite=False):
                self._rewrite = rewrite

            def set_up(self):
                print(f"Load web page at {self.given['website']}")

            def form_filled(self, **textboxes):
                for name, contents in sorted(textboxes.items()):
                    print(f"Put {contents} in name")

            def clicked(self, name):
                print(f"Click on {name}")
            
            def failing_step(self):
                raise Failure("This was not supposed to happen")
            
            def error_message_displayed(self, expected_message):
                """Demonstrates steps that can rewrite themselves."""
                actual_message = "error message!"
                try:
                    strings_match(expected_message, actual_message)
                except Failure:
                    if self._rewrite:
                        self.current_step.rewrite("expected_message").to(actual_message)
                    else:
                        raise

            def email_was_sent(self):
                print("Check email was sent!")

  steps:
  - Run:
      code: |
        from hitchstory import StoryCollection
        from pathlib import Path
        from engine import Engine

        StoryCollection(Path(".").glob("*.story"), Engine()).named("Email sent").play()
      will output: |-
        RUNNING Email sent in /path/to/working/example.story ... Load web page at /login
        Put hunter2 in name
        Put AzureDiamond in name
        Click on login
        Click on new email
        Put Hey guys,

        I think I got hacked!
         in name
        Put Cthon98@aol.com in name
        Click on send email
        Check email was sent!
        SUCCESS in 0.1 seconds.
