---
title: Snapshot Test Driven Development (STDD)
---
# Snapshot Test Driven Development (STDD)

Snapshot test driven development is a combination of **snapshot testing** and **test driven development**.

It is often an ideal methodology to use when orthodox test driven development doesn't work.


## Process

The developer ***writes a test that sets up a scenario** that *should* produce the desired result but without defining a result in the test.

This scenario could be "log in, click on report link, report appears".

They then run the **failing test** in **normal mode** - validating that it sets up the scenario correctly.

They then run the test in **rewrite mode** - adjusting the result based upon what the program does. e.g. taking a screenshot of the new dashboard or saving textual output to the test.

The developer then adjusts the code, eyeballing the result, committing it only once they are satisfied with the result - e.g. the dashboard looks correct.

Future ordinary test runs (e.g. on CI) will compare the snapshot with actual output and fail if anything has changed.




## Examples

These are four example projects built with hitchstory, all of which are set up to do snapshot test driven development:

- [Command line](https://github.com/hitchdev/hitchstory/tree/master/examples/commandline) - the screenshot steps in an interactive command line test validate a command line "screenshot" which will be rewritten in rewrite mode.

- [REST API](https://github.com/hitchdev/hitchstory/tree/master/examples/restapi) - in rewrite mode, the responses from the REST API are rewritten when the code changes.

- [Website](https://github.com/hitchdev/hitchstory/tree/master/examples/website) - the output in the "expect" step is rewritten in rewrite mode. E.g. expect "error message" in error label and the screenshots are compared.

- [Python API](https://github.com/hitchdev/hitchstory/tree/master/examples/pythonapi) - the results of print statements are captured in these tests and can be rewritten.




## When to do it?

Orthodox unit test driven development works extremely well for a specific set of circumstances - perhaps even more specific:

- The outputs are clear and relatively simple and you know precisely what they should be, for example the result of a calculation.
- The inputs are clear and relatively simple.
- The code is stateless and functional.

Not all development is like this though. It is very common - perhaps more common even for the developer to have:

- A clear picture of the scenario.
- A fuzzy idea about what the output should be.
- But to be clear about what they want when they see it.

In this case, snapshot test driven development works extremely well.




## Integration vs. Unit Tests

Snapshot test driven development generally works better for the kind of scenarios which are integration tested.



