from pathlib import Path

ROOT = Path(__file__).absolute().parents[0].parent


class DIR:
    PROJECT = ROOT
    APP = ROOT / "app"
    ARTEFACTS = ROOT / "artefacts"
    DOCS = ROOT / "hitch" / "docs"
    STORY = ROOT / "hitch" / "story"
    DATACACHE = Path("/gen")
    TESTS = ROOT / "hitch"