def run_docgen(paths, storybook):
    storydocs = storybook.with_documentation(
        paths.key.joinpath("docstory.yml").text(),
        extra={"in_interpreter": False, "include_title": True},
    )

    for story in storydocs.ordered_by_file():
        docfilename = story.info.get("docs")
        if docfilename is not None:
            docpath = paths.project.joinpath(
                "docs", "public", "using", docfilename + ".md"
            )
            docpath.write_text(story.documentation())
