---
title: Specification Documentation Test Triality
---
# Specification Documentation Test Triality

Triality is a development and automation process enabled by hitchstory where you maintain *single source of truth* for your specifications, tests and docs.

The specifications are executable, and are executed with a story engine. With some templating they can also be used to autogenerate text based documentation (e.g. markdown, HTML).

This form of automation fixes three common problems:

- It can make sure that documentation, tests and specs will all get actually get written - none will exist or all will exist.
- They won't go out of date - the examples are tested by CI and will fail if changed.
- Less boredom. With triality the really tedious parts of documentation, testing and specifying are automated.

# Simple real life example

[I built this simple command line app](https://github.com/crdoconnor/orji) to scratch an itch - I wanted to generate a pretty LaTeX letter from the org mode output of [my favorite mobile note taking app](https://f-droid.org/packages/com.orgzly/).

One feature I added to this app was the ability to convert the org mode markup - links, bold, italics, etc. into markdown.

This feature is documented with a [a simple how to page](https://hitchdev.com/orji/using/markdown/). The web page is static HTML, generated using the excellent [mkdocs](https://www.mkdocs.org/) from [a markdown document](https://github.com/crdoconnor/orji/blob/main/docs/public/using/markdown.md) using the mkdocs flavor of markdown.

So far, so normal - lots of projects have how to documentation like this written by hand.

This markdown document was generated, however, using a combination of [custom jinja2 templates](https://github.com/crdoconnor/orji/blob/main/hitch/docstory.yml) and the [executable specification for this feature](https://github.com/crdoconnor/orji/blob/main/hitch/story/markdown.story).

While 

# Is this tool able to autogenerate *all* my documentation?

No.

According to the [Diátaxis](https://diataxis.fr/) model there are 4 broad types of documentation necessary for a software project.

While HitchStory can probably be used to autogenerate most how-to documentation there is some stuff like explanations or project justifications that a human should write. Fortunately this sort of thing doesnt go out of date as quickly and is more interesting to write.

Even for the generated how to documentation to be good you will often need to add clear and thoughtful high level explanations to accompany the examples that exhibit the features.

# Isn't this what Cucumber tried to do?

No.

Cucumber's model treated specifications and documentation as the same thing. Moreover, due to the design of the DSL and the culture around the tool it made it very difficult if not impossible to produce specifications with complex preconditions and steps.

The users of the tool ended up pushing down specification details to the execution code where only the tool writers could see it.

This has led most people who use the tool to give up on it.

Hitchstory model : Behavior <---> Execution

Cucumber model : High level spec <--> Munged low level spec and execution code.

# What about screenshots?

If the executable specifications are executed something like appium or playwright you can generate screenshot artefacts as a result of running the suite of tests.

The markdown/HTML/whatever documentation generated could then directly reference these files as images.

# What could I use this for?

There are many uses for specification to documentation autogeneration, including:

- Generating how-to docs for your REST API for use by mobile app developers.
- Generating how to docs for a python library (all of the projects on this website are produced this way).
- Generating detailed reports to show to upper management to demonstrate your app's capabilities without requiring a meeting.
- Generating documentation showing all user flows on a multi-language website that can be quality controlled by a translator.
- Generating reports for regulators to demonstrate that an application has undergone rigorous testing.
- ...and much more.


