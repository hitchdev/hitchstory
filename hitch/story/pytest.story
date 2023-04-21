Using hitchstory with pytest:
  based on: quickstart
  about: |
    If you already have pytest set up and a full
    suite of integration tests and would like to dip
    your toe in the water with hitchstory, you
    can easily run stories directly from inside pytest
    without any plugins.

    This example demonstrates the stories from the
    README being run from inside pytest.
  given:
    files:
      test_integration.py: |
        from hitchstory import StoryCollection
        from pathlib import Path
        from engine import Engine

        hs = StoryCollection(
            # All *.story files in this test's directory
            Path(__file__).parent.glob("*.story"), 
            Engine()
        )

        def test_email_sent():
            hs.named("Email sent").play()

        def test_logged_in():
            hs.named("Logged in").play()
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



