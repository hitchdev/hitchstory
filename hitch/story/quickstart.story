Quickstart:
  given:
    files:
      example.story: |
        Log in as James:
          given:
            browser: firefox  # preconditions
          steps:
          - Enter text:
              username: james
              password: password
          - Click: log in
          
        See James analytics:
          based on: log in as james  # inheritance
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

        #Manually run stories within pytest tests
        #def test_log_in_as_james():
        #    collection.named("Log in as james").play()

        #def test_see_james_analytics():
        #    collection.named("See James analytics").play()

        # Automagically add all stories as tests.
        # E.g. "Log in as James" -> "def test_login_in_as_james"
        collection.with_external_test_runner().ordered_by_name().add_pytests_to(
            module=__import__(__name__) # This module
        )
  variations:
    Run log in as James test:
      about: |
        This runs "test_log_in_as_james", a pytestified version of "Log in as James".
        
        -s allows you to see the printed output.
      steps:
      - pytest:
          args: -s test_hitchstory.py -k test_log_in_as_james
          will output: |-
            ============================= test session starts ==============================
            platform linux -- Python n.n.n, pytest-n.n.n, pluggy-n.n.n
            rootdir: /path/to
            collected 2 items / 1 deselected / 1 selected

            test_hitchstory.py Using browser firefox
            Enter james in username
            Enter password in password
            Click on log in
            .

            ======================= 1 passed, 1 deselected in 0.1s ========================

    Run failing test:
      about: |
        Failing tests look like this but with highlighting and more colorful.
      steps:
      - pytest:
          expect failure: yes
          args: -k test_see_james_analytics test_hitchstory.py
          will output: |-
            ============================= test session starts ==============================
            platform linux -- Python n.n.n, pytest-n.n.n, pluggy-n.n.n
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
            E             based on: log in as james  # inheritance
            E             following steps:
            E             - Click: analytics
            E
            E
            E       hitchstory.exceptions.Failure
            E
            E           Test failed.
            E
            E       button analytics not found

            /src/hitchstory/story_list.py:50: StoryFailure
            ----------------------------- Captured stdout call -----------------------------
            Using browser firefox
            Enter james in username
            Enter password in password
            Click on log in
            Click on analytics
            =========================== short test summary info ============================
            FAILED test_hitchstory.py::test_see_james_analytics - hitchstory.exceptions.StoryFailure: RUNNING See James analytics in /path/to/example.story ... FAILED in 0.1 seconds.

                  based on: log in as james  # inheritance
                  following steps:
                  - Click: analytics


            hitchstory.exceptions.Failure

                Test failed.

            button analytics not found
            ======================= 1 failed, 1 deselected in 0.1s ========================
