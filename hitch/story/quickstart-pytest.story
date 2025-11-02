Pytest Quickstart:
  about: |
    Minimal example (two files) demonstrating two short YAML tests and the 
    python code necessary to run them from within a pytest file.
  given:
    files:
      example.story: |
        Log in as James:
          given:
            browser: firefox  # test preconditions
          steps:
          - Enter text:
              username: james
              password: password
          - Click: log in
          
        See James analytics:
          based on: log in as james  # test inheritance
          following steps:
          - Click: analytics
      test_hitchstory.py: |
        from hitchstory import BaseEngine, GivenDefinition, GivenProperty
        from hitchstory import Failure, strings_match
        from hitchstory import StoryCollection
        from strictyaml import Str
        from pathlib import Path
        from os import getenv

        class Engine(BaseEngine):
            """Interprets and validates the hitchstory stories."""

            given_definition = GivenDefinition(
                browser=GivenProperty(
                    # Available validators: https://hitchdev.com/strictyaml/using/
                    Str()
                ),
            )
            
            def __init__(self, rewrite=False):
                self._rewrite = rewrite

            def set_up(self):
                print(f"Using browser {self.given['browser']}")

            def click(self, name):
                print(f"Click on {name}")
                
                if name == "analytics":
                    raise Failure(f"button {name} not found")
            
            def enter_text(self, **textboxes):
                for name, text in textboxes.items():
                    print(f"Enter {text} in {name}")
            
            def tear_down(self):
                pass


        collection = StoryCollection(
            # All .story files in this file's directory.
            Path(__file__).parent.glob("*.story"),

            Engine(
                # If REWRITE environment variable is set to yes -> rewrite mode.
                rewrite=getenv("REWRITE", "no") == "yes"
            )
        )

        #You can embed the stories in tests manually:
        #def test_log_in_as_james():
        #    collection.named("Log in as james").play()

        #def test_see_james_analytics():
        #    collection.named("See James analytics").play()

        # Or autogenerate runnable tests from the YAML stories like so:
        # E.g. "Log in as James" -> "def test_login_in_as_james"
        collection.with_external_test_runner().ordered_by_name().add_pytests_to(
            module=__import__(__name__) # This module
        )
  variations:
    Run passing "log in as James" test:
      about: |
        Running test_log_in_as_james runs the "Log in as James" story.
      steps:
      - pytest:
          args: -s -k test_log_in_as_james
          will output: |-
            ============================= test session starts ==============================
            platform linux -- Python n.n.na1, pytest-n.n.n, pluggy-n.n.n
            rootdir: /path/to
            collected 2 items / 1 deselected / 1 selected

            test_hitchstory.py Using browser firefox
            Enter james in username
            Enter password in password
            Click on log in
            .

            ======================= 1 passed, 1 deselected in 0.1s ========================

    Run failing "see James' analytics" test:
      about: |
        Failing tests also have colors and highlighting when run for real.
      steps:
      - pytest:
          expect failure: yes
          args: -k test_see_james_analytics
          will output: |-
            ============================= test session starts ==============================
            platform linux -- Python n.n.na1, pytest-n.n.n, pluggy-n.n.n
            rootdir: /path/to
            collected 2 items / 1 deselected / 1 selected

            test_hitchstory.py F                                                     [100%]

            =================================== FAILURES ===================================
            ___________________________ test_see_james_analytics ___________________________

            story = Story('see-james-analytics')

                def hitchstory(story=story):
            >       story.play()
            E       hitchstory.exceptions.StoryFailure: RUNNING See James analytics in /path/to/example.story ... FAILED in 0.1 seconds.
            E
            E             based on: log in as james  # test inheritance
            E             following steps:
            E             - Click: analytics
            E
            E
            E       hitchstory.exceptions.Failure
            E
            E       Test failed.
            E
            E       button analytics not found

            /src/hitchstory/story_list.py:51: StoryFailure
            ----------------------------- Captured stdout call -----------------------------
            Using browser firefox
            Enter james in username
            Enter password in password
            Click on log in
            Click on analytics
            =========================== short test summary info ============================
            FAILED test_hitchstory.py::test_see_james_analytics - hitchstory.exceptions.StoryFailure: RUNNING See James analytics in /path/to/example.story ... FAILED in 0.1 seconds.

                  based on: log in as james  # test inheritance
                  following steps:
                  - Click: analytics


            hitchstory.exceptions.Failure

            Test failed.

            button analytics not found
            ======================= 1 failed, 1 deselected in 0.1s ========================
