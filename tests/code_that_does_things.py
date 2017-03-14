import sys


class ExampleException(Exception):
    """
    This is a demonstration exception's docstring.

    It spreads across multiple lines.
    """
    pass


def should_run(which):
    with open("should{0}.txt".format(which), "w") as handle:
        handle.write("ran!")


def should_not_run():
    raise RuntimeError("This shouldn't have happened")


def raise_example_exception(text=""):
    raise ExampleException(text)


def output(contents):
    with open("output.txt", 'w') as handle:
        handle.write("{0}\n".format(contents))


def append(contents):
    with open("output.txt", 'a') as handle:
        handle.write("{0}\n".format(contents))


def reticulate_splines():
    with open("splines_reticulated.txt", 'w') as handle:
        handle.write("{0}\n".format("splines_reticulated"))


def kick_llamas_ass():
    with open("kicked_llamas_ass.txt", 'w') as handle:
        handle.write("{0}\n".format("kicked_llamas_ass"))
