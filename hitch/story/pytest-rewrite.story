Self rewriting tests with pytest and hitchstory:
  docs: pytest/rewrite
  based on: quickstart
  given:
    files:
      failure.story: |
        Failing story:
          given:
            website: /login  # preconditions
          steps:
          - Failing step
      rewritable.story: |
        Rewritable story:
          given:
            website: /error
          steps:
          - Error message displayed: old message

      test_integration.py: |
        from hitchstory import StoryCollection
        from pathlib import Path
        from engine import Engine
        import os

        hs = StoryCollection(
            # All *.story files in this test's directory
            Path(__file__).parent.glob("*.story"),
            
            # Rewrite if REWRITE environment variable is set to yes
            Engine(rewrite=os.getenv("REWRITE", "") == "yes")
        ).with_external_test_runner()

        def test_email_sent():
            hs.named("Email sent").play()

        def test_logged_in():
            hs.named("Logged in").play()
            
      test_other.py: |
        from hitchstory import StoryCollection
        from pathlib import Path
        from engine import Engine
        import os

        hs = StoryCollection(
            # All *.story files in this test's directory
            Path(__file__).parent.glob("*.story"),

            # Rewrite if REWRITE environment variable is set to yes
            Engine(rewrite=os.getenv("REWRITE", "") == "yes")
        ).with_external_test_runner()

        def test_failure():
            hs.named("Failing story").play()

        def test_rewritable():
            hs.named("Rewritable story").play()

  variations:
    Run all passing tests:
      about: |
        This runs the two tests in test_integration.py.
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

    Rewrite story:
      about: |
        By setting the environment variable REWRITE to "yes",
        pytest can be configured to run tests in rewrite mode.

        The only story configured to rewrite itself currently
        is test_rewritable in test_other.py:
      replacement steps:
      - pytest:
          env:
            REWRITE: yes
          args: -k test_rewritable test_other.py
          will output: |-
            ============================= test session starts ==============================
            platform linux -- Python n.n.n, pytest-n.n.n, pluggy-n.n.n
            rootdir: /path/to
            collected 2 items / 1 deselected / 1 selected

            test_other.py .                                                          [100%]

            ======================= 1 passed, 1 deselected in 0.1s ========================

      - File contents will be:
          folder: state
          filename: rewritable.story
          contents: |-
            Rewritable story:
              given:
                website: /error
              steps:
              - Error message displayed: error message!

    Failing test:
      about: |
        Failing tests will result in a StoryFailure exception being
        raised.

        The message within the exception will contain details of the
        step where the test failed.

        For most exceptions (not this one), there will be a stack
        trace displayed as well.

        Note that the [[ COLOR ]] will be replaced with actual colors
        if this is run on the command line.
      replacement steps:
      - pytest:
          args: -k test_failure test_other.py
          expect failure: yes
          will output: |-
            ============================= test session starts ==============================
            platform linux -- Python n.n.n, pytest-n.n.n, pluggy-n.n.n
            rootdir: /path/to
            collected 2 items / 1 deselected / 1 selected

            test_other.py F                                                          [100%]

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

            test_other.py:15: StoryFailure
            ----------------------------- Captured stdout call -----------------------------
            Load web page at /login
            =========================== short test summary info ============================
            FAILED test_other.py::test_failure - hitchstory.exceptions.StoryFailure: RUNNING Failing story in /path/to/failure.story ... [[ RED ]][[ BRIGHT ]]FAILED in 0.1 seconds.[[ RESET ALL ]]

            [[ BLUE ]]        website: /login  # preconditions
                  steps:
                [[ BRIGHT ]]  - Failing step[[ NORMAL ]]
                [[ RESET ALL ]]

            [[ RED ]][[ BRIGHT ]]hitchstory.exceptions.Failure[[ RESET ALL ]]
              [[ DIM ]][[ RED ]]
                Test failed.
                [[ RESET ALL ]]
            [[ RED ]]This was not supposed to happen[[ RESET FORE ]]
            ======================= 1 failed, 1 deselected in 0.1s ========================
