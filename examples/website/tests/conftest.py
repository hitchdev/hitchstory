from os import getenv
from docgen import generate_docs
from commandlib import python_bin
from directories import DIR


def pytest_sessionfinish(session, exitstatus):
    """Run after all tests have run - regenerate markdown docs?"""
    if exitstatus == 0:
        if getenv("STORYMODE", "") == "rewrite":
            generate_docs()

        if getenv("STORYMODE", "") == "coverage":
            combined_file = DIR.APP / "combined.coverage"
            if combined_file.exists():
                combined_file.unlink()
            coverage_files = list(DIR.ARTEFACTS.glob("*.coverage"))

            python_bin.coverage(
                "combine", "--keep", f"--data-file={combined_file}", *coverage_files
            ).in_dir(DIR.APP).output()

            python_bin.coverage(
                "html",
                "--data-file=combined.coverage",
                f"--directory={DIR.ARTEFACTS}/htmlcov",
            ).in_dir(DIR.APP).output()

            python_bin.coverage(
                "xml",
                "--data-file=combined.coverage",
                "-o",
                f"{DIR.ARTEFACTS}/coverage.xml",
            ).in_dir(DIR.APP).output()
