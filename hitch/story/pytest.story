Using hitchstory with pytest:
  docs: pytest
  based on: quickstart
  about: |
    If you already have pytest set up and a full
    suite of integration tests and would like to dip
    your toe in the water with hitchstory, you
    can easily run stories directly from inside pytest.

    The following files - engine.py, the .story files
    can all be put in the same folder.
  given:
    files:
      failure.story: |
        Failing story:
          given:
            website: /login  # preconditions
          steps:
          - Failing step

      test_failure.py: |
        from hitchstory import StoryCollection
        from pathlib import Path
        from engine import Engine
        import os

        hs = StoryCollection(
            # All *.story files in this test's directory
            Path(__file__).parent.glob("*.story"), 
            Engine(rewrite=os.getenv("REWRITE", "") == "yes")
        ).with_external_test_runner()

        def test_failure():
            hs.named("Failing story").play()

      test_integration.py: |
        from hitchstory import StoryCollection
        from pathlib import Path
        from engine import Engine

        hs = StoryCollection(
            # All *.story files in this test's directory
            Path(__file__).parent.glob("*.story"), 
            Engine()
        ).with_external_test_runner()

        def test_email_sent():
            hs.named("Email sent").play()

        def test_logged_in():
            hs.named("Logged in").play()
  variations:
    Run all tests:
      replacement steps:
      - pytest:
          args: test_integration.py
          will output: |-
            ============================= test session starts ==============================
            platform linux -- Python n.n.n, pytest-n.n.n, pluggy-n.n.n
            rootdir: /path/to
            collected 2 items

            test_integration.py ..                                                   [100%]

            ============================== 2 passed in 0.1s ===============================

    Failing test:
      replacement steps:
      - pytest:
          args: test_failure.py
          expect failure: yes
          will output: |-
            ============================= test session starts ==============================
            platform linux -- Python n.n.n, pytest-n.n.n, pluggy-n.n.n
            rootdir: /path/to
            collected 1 item

            test_failure.py F                                                        [100%]

            =================================== FAILURES ===================================
            _________________________________ test_failure _________________________________

                def test_failure():
            >       hs.named("Failing story").play()
            E       hitchstory.exceptions.StoryFailure: RUNNING Failing story in /path/to/failure.story ... [[ RED ]][[ BRIGHT ]]FAILED in 0.1 seconds.[[ RESET ALL ]]
            E
            E       [[ BLUE ]]        website: /login  # preconditions
            E             steps:
            E           [[ BRIGHT ]]  - Failing step[[ NORMAL ]]
            E           [[ RESET ALL ]]
            E
            E       [[ RED ]][[ BRIGHT ]]hitchstory.exceptions.Failure[[ RESET ALL ]]
            E         [[ DIM ]][[ RED ]]
            E           Test failed.
            E           [[ RESET ALL ]]
            E       [[ RED ]]This was not supposed to happen[[ RESET FORE ]]

            test_failure.py:12: StoryFailure
            ----------------------------- Captured stdout call -----------------------------

            Visiting http://localhost:5000/login
            =========================== short test summary info ============================
            FAILED test_failure.py::test_failure - hitchstory.exceptions.StoryFailure: RUNNING Failing story in /path/to/failure.story ... [[ RED ]][[ BRIGHT ]]FAILED in 0.1 seconds.[[ RESET ALL ]]

            [[ BLUE ]]        website: /login  # preconditions
                  steps:
                [[ BRIGHT ]]  - Failing step[[ NORMAL ]]
                [[ RESET ALL ]]

            [[ RED ]][[ BRIGHT ]]hitchstory.exceptions.Failure[[ RESET ALL ]]
              [[ DIM ]][[ RED ]]
                Test failed.
                [[ RESET ALL ]]
            [[ RED ]]This was not supposed to happen[[ RESET FORE ]]
            ============================== 1 failed in 0.1s ===============================
