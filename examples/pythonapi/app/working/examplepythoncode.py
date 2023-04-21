# -*- coding: utf-8 -*-
import sys


if sys.version_info[0] == 3:
    unicode = str


def _save_exception():
    import json
    from os.path import abspath

    tb_id = 0
    _, exception, tb = sys.exc_info()

    if exception is None:
        return None

    # Create list of tracebacks
    tracebacks = []
    while tb is not None:
        filename = tb.tb_frame.f_code.co_filename
        if filename == "<frozen importlib._bootstrap>":
            break

        tracebacks.append(
            {
                "tb_id": tb_id,
                "filename": abspath(tb.tb_frame.f_code.co_filename),
                "line": tb.tb_lineno,
                "function": tb.tb_frame.f_code.co_name,
            }
        )

        tb_id = tb_id + 1
        tb = tb.tb_next

    with open("/src/app/working/error.txt", "w") as handle:
        handle.write(
            json.dumps(
                {
                    "tracebacks": tracebacks,
                    "exception_string": unicode(exception),
                    "docstring": exception.__doc__
                    if exception.__doc__ is not None
                    else None,
                    "exception_type": "{}.{}".format(
                        type(exception).__module__, type(exception).__name__
                    ),
                    "event": "exception",
                }
            )
        )


try:

    def run_example_code():
        def runcode():
            import todo

            todo.new("buy bread")

        runcode()

    run_example_code()
except Exception as error:
    _save_exception()
    sys.exit(0)
