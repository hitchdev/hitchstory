def run_docgen(paths, storybook):
    storydocs = storybook.with_documentation(paths.key.joinpath("docstory.yml").text())

    for story in storydocs:
        docfilename = story.info.get("docs")
        if docfilename is not None:
            docpath = paths.joinpath(
                "docs", "public", "using", "alpha", docfilename + ".md"
            )
            # docpath.write_text(story.documentation())
