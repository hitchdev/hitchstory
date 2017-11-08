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

def tear_down_was_run():
    with open("tear_down_was_run.txt", 'w') as handle:
        handle.write("{0}\n".format("tear_down_was_run"))
    
def fill_form(name, value):
    with open("{0}.txt".format(name), 'w') as handle:
        handle.write(value)

def click(name):
    with open("click.txt".format(name), 'a') as handle:
        handle.write(name)
