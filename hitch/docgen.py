from strictyaml import load
from commandlib import python_bin


README_INTRO = """# HitchStory

[![Main branch status](https://github.com/hitchdev/hitchstory/actions/workflows/regression.yml/badge.svg)](https://github.com/hitchdev/hitchstory/actions/workflows/regression.yml)"""

DOCS_INTRO = """---
title: HitchStory
---

![](sliced-cucumber.jpg)

<img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/hitchdev/hitchstory?style=social"> 
<img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/hitchstory">
"""


def _title(filepath):
    assert len(filepath.text().split("---")) >= 3, "{} doesn't have ---".format(
        filepath
    )
    return load(filepath.text().split("---")[1]).data.get("title", "misc")


def _contents(main_folder, folder):
    markdown = ""
    for filepath in sorted(main_folder.joinpath(folder).listdir()):
        if filepath.name != "index.md":
            filepath.name.stripext()
            markdown += "- [{}]({})\n".format(
                _title(filepath),
                filepath.relpath(main_folder).stripext(),
            )
    return markdown


def run_docgen(paths, storybook):
    dirtempl = python_bin.dirtempl.in_dir(paths.project / "docs")
    doc_src = paths.project / "docs" / "src"
    dest_path = paths.project / "docs" / "draft"
    snippets_path = paths.project / "docs" / "snippets"

    if snippets_path.exists():
        snippets_path.rmtree()
    snippets_path.mkdir()

    if dest_path.exists():
        dest_path.rmtree()

    snippets_path.joinpath("quickstart.txt").write_text(
        storybook.with_documentation(
            paths.key.joinpath("docstory.yml").text(),
            extra={"in_interpreter": True, "include_title": False},
        )
        .named("Quickstart")
        .documentation()
    )

    generate_storydocs(
        paths.key.joinpath("docstory.yml").text(),
        doc_src.joinpath("using"),
        storybook,
    )

    snippets_path.joinpath("intro.txt").write_text(DOCS_INTRO)
    snippets_path.joinpath("why-contents.txt").write_text(_contents(doc_src, "why"))
    snippets_path.joinpath("why-not-contents.txt").write_text(
        _contents(doc_src, "why-not")
    )
    snippets_path.joinpath("approach-contents.txt").write_text(
        _contents(doc_src, "approach")
    )
    snippets_path.joinpath("using-contents.txt").write_text(_contents(doc_src, "using"))
    dirtempl("--snippets", "snippets", "src", dest_path).run()


def generate_storydocs(docstory, docpath, storybook):
    storydocs = storybook.with_documentation(
        docstory,
        extra={"in_interpreter": False, "include_title": True},
    )

    for story in storydocs.ordered_by_file():
        docfilename = story.info.get("docs")
        if docfilename is not None:
            docpath.joinpath(docfilename + ".md").write_text(story.documentation())
