---
title: Snapshot Test Driven Development
---
# Snapshot Test Driven Development

Snapshot test driven development is a combination of test driven development and snapshot testing.

The developer writes a test that sets up a scenario that produces an output that is inexactly defined - e.g. a GUI, a command line output.

They then adjust the code to produce something closer to the desired output and run the test in rewrite mode - this keeps a snapshot of the output.

Once the developer (and stakeholders) are happy with the result, the test, snapshot and code are committed.

From that point on the test will check that the snapshot matches the actual output.


## Examples

There are four example projects built with hitchstory, all of which are set up to do snapshot test driven development:

 * [Command line](https://github.com/hitchdev/hitchstory/tree/master/examples/commandline) - the screenshot steps in an interactive command line test validate a command line "screenshot" which will be rewritten in rewrite mode.

 * [REST API](https://github.com/hitchdev/hitchstory/tree/master/examples/restapi) - the responses from the REST API are  rewritten when the code changes.

 * [Website](https://github.com/hitchdev/hitchstory/tree/master/examples/website) - the output in the "expect" step is rewritten in rewrite mode. E.g. expect "error message" in error label and the screenshots are compared.

 * [Python API](https://github.com/hitchdev/hitchstory/tree/master/examples/pythonapi) - the results of print statements are captured in these tests and can be rewritten.




## When to do it?

Orthodox test driven development works extremely well for a very specific set of circumstances:

- The outputs are clear and relatively simple and you know exactly what they should be (e.g. result of a calculation).
- The inputs are clear and relatively simple.
- The code is stateless and functional.

Not all development is like this though. In many (perhaps more) cases the developer will have a rough idea of the output.

In this case, snapshot test driven development can be extremely helpful - it is used to set up a scenario which should lead to the desired output and then the developer can switch to modifying the code and eyeballing the result to see if it is correct.



