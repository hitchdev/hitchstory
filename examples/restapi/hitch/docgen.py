from strictyaml import load
from commandlib import Command, python_bin
import hitchpylibrarytoolkit


README_INTRO = """# OrJi

[![Main branch status](https://github.com/crdoconnor/orji/actions/workflows/regression.yml/badge.svg)](https://github.com/crdoconnor/orji/actions/workflows/regression.yml)"""

DOCS_INTRO = """---
title: OrJi
---

<a href="https://github.com/crdoconnor/orji"><img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/crdoconnor/orji?style=social"/></a>

<a href="https://pypi.org/pypi/orji"><img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/orji"/></a>
"""


def _title(filepath):
    try:
        assert len(filepath.text().split("---")) >= 3, "{} doesn't have ---".format(
            filepath
        )
        return load(filepath.text().split("---")[1]).data.get("title", "misc")
    except UnicodeDecodeError:
        return None
    except AssertionError:
        return None


def _contents(main_folder, folder, readme):
    markdown = ""
    for filepath in sorted(main_folder.joinpath(folder).listdir()):
        if filepath.name != "index.md":
            title = _title(filepath)

            if title is not None:
                path = filepath.relpath(main_folder).stripext()

                markdown += "- [{}]({})\n".format(
                    title,
                    "https://hitchdev.com/orji/" + path if readme else path,
                )
    return markdown


def run_docgen(paths, storybook, publish=False, readme=False):
    dirtempl = python_bin.dirtempl.in_dir(paths.project / "docs")
    doc_src = paths.project / "docs" / "src"
    snippets_path = paths.project / "docs" / "snippets"
    git = Command("git").in_dir(paths.project)

    if publish:
        dest_path = paths.gen / "orji" / "docs" / "public"
    else:
        dest_path = paths.project / "docs" / "draft"

    if snippets_path.exists():
        snippets_path.rmtree()
    snippets_path.mkdir()

    if dest_path.exists():
        dest_path.rmtree()

    snippets_path.joinpath("quickstart.txt").write_text(
        storybook.with_documentation(
            paths.key.joinpath("docstory.yml").text(),
            extra={"title": False},
        )
        .named("Quickstart")
        .documentation()
    )

    generate_storydocs(
        paths.key.joinpath("docstory.yml").text(),
        doc_src.joinpath("using"),
        storybook,
    )

    snippets_path.joinpath("intro.txt").write_text(
        README_INTRO if readme else DOCS_INTRO
    )

    for folder in ["using"]:
        snippets_path.joinpath(f"{folder}-contents.txt").write_text(
            _contents(doc_src, folder, readme=readme)
        )

    for folder in ["using"]:
        snippets_path.joinpath(f"{folder}-index-contents.txt").write_text(
            _contents(doc_src / folder, "", readme=readme)
        )

    dirtempl("--snippets", snippets_path, doc_src, dest_path).run()

    dest_path.joinpath("changelog.md").write_text(
        hitchpylibrarytoolkit.docgen.changelog(paths.project)
    )


def generate_storydocs(docstory, docpath, storybook):
    storydocs = storybook.with_documentation(
        docstory,
        extra={"title": True},
    )

    for story in storydocs.ordered_by_file():
        docfilename = story.info.get("docs")
        if docfilename is not None:
            docpath.joinpath(docfilename + ".md").write_text(story.documentation())
