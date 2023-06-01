from os import getenv
from docgen import generate_docs
from pathlib import Path
from commandlib import python_bin


PROJECT_DIR = Path(__file__).absolute().parents[0].parent
ARTEFACTS_DIR = PROJECT_DIR.joinpath("artefacts")


def pytest_sessionfinish(session, exitstatus):
    """Run after all tests have run - regenerate markdown docs?"""
    if exitstatus == 0:
        if getenv("STORYMODE", "") == "rewrite":
            generate_docs()

        if getenv("STORYMODE", "") == "coverage":
            combined_file = PROJECT_DIR.joinpath("app", "combined.coverage")
            if combined_file.exists():
                combined_file.unlink()
            coverage_files = list(PROJECT_DIR.joinpath("artefacts").glob("*.coverage"))

            python_bin.coverage(
                "combine", "--keep", f"--data-file={combined_file}", *coverage_files
            ).in_dir(PROJECT_DIR / "app").output()

            python_bin.coverage(
                "html",
                "--data-file=combined.coverage",
                f"--directory={ARTEFACTS_DIR}/htmlcov",
            ).in_dir(PROJECT_DIR / "app").output()

            python_bin.coverage(
                "xml",
                "--data-file=combined.coverage",
                "-o",
                f"{ARTEFACTS_DIR}/coverage.xml",
            ).in_dir(PROJECT_DIR / "app").output()
