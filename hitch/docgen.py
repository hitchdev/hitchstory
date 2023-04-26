from strictyaml import load
from commandlib import Command, python_bin
import hitchpylibrarytoolkit


class ProjectDocumentation:
    def __init__(
        self,
        storybook,
        project_path,
        publish_path,
        project_name,
        github_address,
        image="",
    ):
        self._storybook = storybook
        self._project_path = project_path
        self._publish_path = publish_path
        self._project_name = project_name
        self._github_address = github_address
        self._project_slug = project_name.lower()
        self._image = image

    def _readme_intro(self):
        return (
            "# {project_name}\n"
            "\n"
            "[![Main branch status](https://github.com/{github_address}/actions/workflows/regression.yml/badge.svg)](https://github.com/{github_address}/actions/workflows/regression.yml)"
        ).format(
            project_name=self._project_name,
            github_address=self._github_address,
        )

    def _docs_intro(self):
        return (
            "---\n"
            "title: {project_name}\n"
            "---\n"
            "\n{image}\n\n"
            '<img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/{github_address}?style=social">'
            '<img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/{project_slug}">'
        ).format(
            image=self._image,
            project_name=self._project_name,
            github_address=self._github_address,
            project_slug=self._project_slug,
        )

    def _title(self, filepath):
        try:
            assert len(filepath.text().split("---")) >= 3, "{} doesn't have ---".format(
                filepath
            )
            return load(filepath.text().split("---")[1]).data.get("title", "misc")
        except UnicodeDecodeError:
            return None
        except AssertionError:
            return None

    def _contents(self, main_folder, folder, readme):
        markdown = ""
        for filepath in sorted(main_folder.joinpath(folder).listdir()):
            if filepath.name != "index.md":
                title = _title(filepath)

                if title is not None:
                    path = filepath.relpath(main_folder).stripext()

                    markdown += "- [{}]({})\n".format(
                        title,
                        "https://hitchdev.com/{}/".format(self._project_slug) + path
                        if readme
                        else path,
                    )
        return markdown

    def generate(self, readme=False):
        dirtempl = python_bin.dirtempl.in_dir(self._project_path / "docs")
        doc_src = self._project_path / "docs" / "src"
        snippets_path = self._project_path / "docs" / "snippets"
        git = Command("git").in_dir(self._project_path)

        dest_path = self._publish_path

        if snippets_path.exists():
            snippets_path.rmtree()
        snippets_path.mkdir()

        if dest_path.exists():
            dest_path.rmtree()

        snippets_path.joinpath("quickstart.txt").write_text(
            self._storybook.with_documentation(
                self._project_path.joinpath("hitch", "docstory.yml").text(),
                extra={"in_interpreter": True, "include_title": False},
            )
            .named("Quickstart")
            .documentation()
        )

        self._generate_storydocs(
            self._project_path.joinpath("hitch", "docstory.yml").text(),
            doc_src.joinpath("using"),
            self._storybook,
        )

        snippets_path.joinpath("intro.txt").write_text(
            self._readme_intro() if readme else self._docs_intro()
        )

        for folder in ["why", "approach", "why-not", "using"]:
            snippets_path.joinpath(f"{folder}-contents.txt").write_text(
                _contents(doc_src, folder, readme=readme)
            )

        for folder in ["why", "approach", "why-not", "using"]:
            snippets_path.joinpath(f"{folder}-index-contents.txt").write_text(
                _contents(doc_src / folder, "", readme=readme)
            )

        dirtempl("--snippets", snippets_path, doc_src, dest_path).run()

        dest_path.joinpath("changelog.md").write_text(
            hitchpylibrarytoolkit.docgen.changelog(self._project_path)
        )

    def _generate_storydocs(self, docstory, docpath, storybook):
        storydocs = storybook.with_documentation(
            docstory,
            extra={"in_interpreter": False, "include_title": True},
        )

        for story in storydocs.ordered_by_file():
            docfilename = story.info.get("docs")
            if docfilename is not None:
                docpath.joinpath(docfilename + ".md").write_text(story.documentation())


README_INTRO = ""

DOCS_INTRO = """---
title: HitchStory
---

![](sliced-cucumber.jpg)

<img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/hitchdev/hitchstory?style=social"> 
<img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/hitchstory">
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
                    "https://hitchdev.com/hitchstory/" + path if readme else path,
                )
    return markdown


def run_docgen(paths, storybook, publish=False, readme=False):
    dirtempl = python_bin.dirtempl.in_dir(paths.project / "docs")
    doc_src = paths.project / "docs" / "src"
    snippets_path = paths.project / "docs" / "snippets"
    git = Command("git").in_dir(paths.project)

    if publish:
        dest_path = paths.gen / "hitchstory" / "docs" / "public"
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

    snippets_path.joinpath("intro.txt").write_text(
        README_INTRO if readme else DOCS_INTRO
    )

    for folder in ["why", "approach", "why-not", "using"]:
        snippets_path.joinpath(f"{folder}-contents.txt").write_text(
            _contents(doc_src, folder, readme=readme)
        )

    for folder in ["why", "approach", "why-not", "using"]:
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
        extra={"in_interpreter": False, "include_title": True},
    )

    for story in storydocs.ordered_by_file():
        docfilename = story.info.get("docs")
        if docfilename is not None:
            docpath.joinpath(docfilename + ".md").write_text(story.documentation())
