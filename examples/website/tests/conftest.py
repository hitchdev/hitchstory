from os import getenv
from docgen import generate_docs

def pytest_sessionfinish(session, exitstatus):
    """Run after all tests have run - regenerate markdown docs?"""
    if exitstatus == 0:
        if getenv("STORYMODE", "") == "rewrite":
            generate_docs()
