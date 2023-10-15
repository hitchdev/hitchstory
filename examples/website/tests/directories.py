from pathlib import Path

ROOT = Path(__file__).absolute().parents[0].parent


class DIR:
    PROJECT = ROOT
    APP = ROOT / "app"
    ARTEFACTS = ROOT / "artefacts"
    DOCS = ROOT / "docs"
    STORY = ROOT / "story"
    SELECTORS = ROOT / "tests" / "selectors"
    DATACACHE = Path("/gen")
