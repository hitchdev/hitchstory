Dip your toe in the water with pytest:
  docs: pytest/dip-your-toe-hitchstory
  based on: quickstart
  about: |
    If you would like to dip your toe into the water
    with hitchstory integration tests, you can `pip install hitchstory`
    and copy and paste the following two files below into a test folder:

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
          
        See James' analytics:
          based on: log in as james  # inheritance
          following steps:
          - Click: analytics
      test_hitchstory.py: |
        from hitchstory import BaseEngine, GivenDefinition, GivenProperty
        from hitchstory import Failure, strings_match
        from hitchstory import StoryCollection
        from pathlib import Path
        from strictyaml import Str
        import os

        class Engine(BaseEngine):
            """Interprets and validates the hitchstory stories."""

            given_definition = GivenDefinition(
                browser=GivenProperty(Str()),
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


        hs = StoryCollection(
            # All *.story files in test_hitchstory.py's directory
            Path(__file__).parent.glob("*.story"),
            
            # If REWRITE environment variable is set to yes -> rewrite mode.
            Engine(rewrite=os.getenv("REWRITE", "") == "yes")
        ).with_external_test_runner()

        def test_log_in_as_james():
            hs.named("Log in as james").play()

        def test_see_james_analytics():
            hs.named("See James' analytics").play()
  variations:
    The log in test passes:
      replacement steps:
      - pytest:
          args: -k test_log_in_as_james test_hitchstory.py
          will output: |-
            ============================= test session starts ==============================
            platform linux -- Python n.n.n, pytest-n.n.n, pluggy-n.n.n
            rootdir: /path/to
            collected 2 items / 1 deselected / 1 selected

            test_hitchstory.py .                                                     [100%]

            ======================= 1 passed, 1 deselected in 0.1s ========================

    See James' analytics test fails:
      replacement steps:
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

                def test_see_james_analytics():
            >       hs.named("See James' analytics").play()
            E       hitchstory.exceptions.StoryFailure: RUNNING See James' analytics in /path/to/example.story ... [[ RED ]][[ BRIGHT ]]FAILED in 0.1 seconds.[[ RESET ALL ]]
            E
            E       [[ BLUE ]]      based on: log in as james  # inheritance
            E             following steps:
            E           [[ BRIGHT ]]  - Click: analytics[[ NORMAL ]]
            E           [[ RESET ALL ]]
            E
            E       [[ RED ]][[ BRIGHT ]]hitchstory.exceptions.Failure[[ RESET ALL ]]
            E         [[ DIM ]][[ RED ]]
            E           Test failed.
            E           [[ RESET ALL ]]
            E       [[ RED ]]button analytics not found[[ RESET FORE ]]

            test_hitchstory.py:47: StoryFailure
            ----------------------------- Captured stdout call -----------------------------
            Using browser firefox
            Enter james in username
            Enter password in password
            Click on log in
            Click on analytics
            =========================== short test summary info ============================
            FAILED test_hitchstory.py::test_see_james_analytics - hitchstory.exceptions.StoryFailure: RUNNING See James' analytics in /path/to/example.story ... [[ RED ]][[ BRIGHT ]]FAILED in 0.1 seconds.[[ RESET ALL ]]

            [[ BLUE ]]      based on: log in as james  # inheritance
                  following steps:
                [[ BRIGHT ]]  - Click: analytics[[ NORMAL ]]
                [[ RESET ALL ]]

            [[ RED ]][[ BRIGHT ]]hitchstory.exceptions.Failure[[ RESET ALL ]]
              [[ DIM ]][[ RED ]]
                Test failed.
                [[ RESET ALL ]]
            [[ RED ]]button analytics not found[[ RESET FORE ]]
            ======================= 1 failed, 1 deselected in 0.1s ========================
