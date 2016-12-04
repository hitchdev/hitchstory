"""
class HitchStacktrace(object):
    def __init__(self, test, where, show_hitch_stacktrace, step=None):
        self.tracebacks = []
        self.test = test
        self.where = where
        if step is not None:
            self.previous_step = test.scenario.steps[step.index - 2] \
                if step.index > 1 else None
            self.next_step = test.scenario.steps[step.index] \
                if step.index < len(test.scenario.steps) else None
        else:
            self.previous_step = None
            self.next_step = None
        self.step = step
        self.show_hitch_stacktrace = show_hitch_stacktrace
        tb_id = 0
        tb = sys.exc_info()[2]
        self.exception = sys.exc_info()[1]

        # Create list of tracebacks
        while tb is not None:
            filename = tb.tb_frame.f_code.co_filename
            if filename == '<frozen importlib._bootstrap>':
                break
            if self.show_hitch_stacktrace or "hitchtest/" not in filename:
                self.tracebacks.append(HitchTraceback(tb_id, tb))
                tb_id = tb_id + 1
            tb = tb.tb_next

    def to_template(self, template="stacktrace_default.jinja2"):
        env = Environment()
        env.loader = FileSystemLoader(TEMPLATE_DIR)
        tmpl = env.get_template(path.basename(template))
        return tmpl.render(
            stacktrace=self.to_dict(),
            TestPosition=TestPosition,
            json=self.to_json(),
            Fore=colorama.Fore,
            Back=colorama.Back,
            Style=colorama.Style,
        )

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {
            'test': self.test.to_dict(),
            'previous_step': self.previous_step.to_dict() \
                if self.previous_step is not None else None,
            'step': self.step.to_dict() if self.step else None,
            'next_step': self.next_step.to_dict() if self.next_step is not None else None,
            'where': self.where,
            'tracebacks': [traceback.to_dict() for traceback in self.tracebacks],
            'exception': str(self.exception),
            'exception_type': "{}.{}".format(
                type(self.exception).__module__, type(self.exception).__name__
            ),
        }

    def __len__(self):
        return len(self.tracebacks)

    def __getitem__(self, index):
        return self.tracebacks[index]



class Traceback(object):
    def __init__(self, tb_id, traceback):
        self.tb_id = tb_id
        self.traceback = traceback

    def to_dict(self):
        return {
            'id': self.tb_id,
            'filename': self.filename(),
            'lineno': self.lineno(),
            'function': self.func(),
            'line': self.loc(),
            'loc_before': self.loc_before(),
            'loc_after': self.loc_after(),
        }

    def filename(self):
        return self.traceback.tb_frame.f_code.co_filename

    def lineno(self):
        return self.traceback.tb_lineno

    def func(self):
        return self.traceback.tb_frame.f_code.co_name

    def localvars(self):
        return self.traceback.tb_frame.f_locals

    def globalvars(self):
        return self.traceback.tb_frame.f_globals

    def frame(self):
        return self.traceback.tb_frame

    def ipython(self):
        utils.ipython(
            message="Entering {} at line {}".format(self.filename(), self.lineno()),
            frame=self.frame(),
        )

    def loc_before(self):
        with open(self.filename(), 'r') as source_handle:
            contents = source_handle.read().split('\n')
        return [
            x for x in enumerate(
                contents[self.lineno() - 3:self.lineno() - 1], self.lineno() - 2
            )
        ]

    def loc(self):
        with open(self.filename(), 'r') as source_handle:
            contents = source_handle.read().split('\n')
        return contents[self.lineno() - 1]

    def loc_after(self):
        with open(self.filename(), 'r') as source_handle:
            contents = source_handle.read().split('\n')
        return [x for x in enumerate(contents[self.lineno():self.lineno() + 2], self.lineno() + 1)]

    def __repr__(self):
        return "[{}] File {}, line {} in {}: {}".format(
            self.tb_id,
            self.filename(),
            self.lineno(),
            self.func(),
            self.loc()
        )

"""
