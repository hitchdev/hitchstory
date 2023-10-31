from pathlib import Path

ROOT = Path(__file__).absolute().parents[0].parent


class DIR:
    PROJECT = ROOT
    APP = ROOT / "app"
    ARTEFACTS = ROOT / "hitch" / "artefacts"
    DOCS = ROOT / "hitch" / "docs"
    STORY = ROOT / "hitch" / "story"
    HITCH = ROOT / "hitch"
    SELECTORS = ROOT / "hitch" / "selectors"
    DATACACHE = Path("/gen")
