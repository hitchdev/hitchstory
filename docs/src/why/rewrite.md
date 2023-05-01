---
title: Why programatically rewrite stories?
---

Programmatic rewriting of stories is a feature that evolved out of
dogfooding the library with stories [like this one](https://github.com/hitchdev/hitchstory/blob/master/hitch/story/fail-fast.story).

Note that the will output section is fairly complicated, but it is possible
to tell at a glance that it is correct.

A normal "approved" TDD approach would be:

1. Write the test first.
2. Write the code that makes it pass.
3. Go to 1.

Ascertaining precisely how that output *should* look when running the code
in advance is not only tedious as hell, it's prone to error.

With hitchstory, you can write tests where hitchstory finishes off the
test for you, by running the test in rewrite mode:

1. Write an incomplete test excluding the output.
2. Write the code that generates the output.
3. Run the test in rewrite mode which changes parts of the story.
4. Eyeball the test.
5. Commit code and story and push and open a PR (which runs the tests in normal mode).

See the [documentation on story rewriting for more details](../../using/engine/rewrite-story).
