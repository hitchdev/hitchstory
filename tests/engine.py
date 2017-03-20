from hitchtest import monitor
from commandlib import run
from simex import DefaultSimex
from os import path
from subprocess import call
import hitchpython
import hitchserve
import hitchtest
import hitchcli
import kaching
import time


class ExecutionEngine(hitchtest.ExecutionEngine):
    """Hitch bootstrap engine tester."""

    def set_up(self):
        self.path.project = self.path.engine.parent
        self.path.state = self.path.engine.parent.joinpath("state")
        self.path.samples = self.path.engine.joinpath("samples")

        if self.path.state.exists():
            self.path.state.rmtree()
        self.path.state.mkdir()

        if self.settings.get("kaching", False):
            kaching.start()

        self.python_package = hitchpython.PythonPackage(
            python_version=self.settings['python_version']
        )
        self.python_package.build()

        self.python = self.python_package.cmd.python
        self.pip = self.python_package.cmd.pip

        self.cli_steps = hitchcli.CommandLineStepLibrary(
            default_timeout=int(self.settings.get("cli_timeout", 5))
        )

        self.cd = self.cli_steps.cd
        self.pexpect_run = self.cli_steps.run
        self.expect = self.cli_steps.expect
        self.send_control = self.cli_steps.send_control
        self.send_line = self.cli_steps.send_line
        self.exit_with_any_code = self.cli_steps.exit_with_any_code
        self.exit = self.cli_steps.exit
        self.finish = self.cli_steps.finish

        run(self.pip("uninstall", "hitchstory", "-y").ignore_errors())

        with monitor([self.path.project.joinpath("setup.py")]) as changed_setup:
            if changed_setup:
                run(self.pip("install", ".").in_dir(self.path.project))
            else:
                run(self.pip("install", ".", "--no-deps").in_dir(self.path.project))

        with monitor([self.path.engine.joinpath("dev_requirements.txt")]) as dev_reqs_changed:
            if dev_reqs_changed:
                run(self.pip("install", "-r", self.path.engine.joinpath("dev_requirements.txt")))

        for filename, contents in self.preconditions.get("files", {}).items():
            self.path.state.joinpath(filename).write_text(contents)
        self.path.state.chdir()

        self.services = hitchserve.ServiceBundle(
            str(self.path.project),
            startup_timeout=8.0,
            shutdown_timeout=1.0
        )

        self.services['IPython'] = hitchpython.IPythonKernelService(self.python_package)

        self.services.startup(interactive=False)
        self.ipython_kernel_filename = self.services['IPython'].wait_and_get_ipykernel_filename()
        self.ipython_step_library = hitchpython.IPythonStepLibrary()
        self.ipython_step_library.startup_connection(self.ipython_kernel_filename)

        self.run_command = self.ipython_step_library.run
        self.assert_true = self.ipython_step_library.assert_true
        self.assert_exception = self.ipython_step_library.assert_exception
        self.shutdown_connection = self.ipython_step_library.shutdown_connection
        self.run_command("import os")
        self.run_command("os.chdir('{}')".format(self.path.state))

        self.path.engine.joinpath("code_that_does_things.py").copy(self.path.state)
        self.run_command("from code_that_does_things import *")

    def lint(self, args=None):
        """Lint the source code."""
        run(self.pip("install", "flake8"))
        run(self.python_package.cmd.flake8(*args).in_dir(self.path.project))

    def run(self, filename="example_code.py"):
        self.path.state.chdir()
        self.pexpect_run("{0} {1}".format(self.python, filename))

    def exit_with_error(self):
        self.exit(with_code=1)

    def exited_successfully(self):
        self.finish()

    def exception_raised(self, command, reference, changeable=None):
        result = self.ipython_step_library.run(command, swallow_exception=True).error
        assert result is not None
        self.path.state.joinpath("output.txt").write_text(result)
        self.output_will_be(reference, changeable)

    def file_was_created_with(self, filename="", contents=""):
        if not self.path.state.joinpath(filename).exists():
            raise RuntimeError("{0} does not exist".format(filename))
        if self.path.state.joinpath(filename).bytes().decode('utf8') != contents:
            raise RuntimeError("{0} did not contain {0}".format(filename, contents))

    def sleep(self, duration):
        """Sleep for specified duration."""
        time.sleep(int(duration))

    def placeholder(self):
        """Placeholder to add a new test."""
        pass

    def splines_reticulated(self):
        assert self.path.state.joinpath("splines_reticulated.txt").exists()
        self.path.state.joinpath("splines_reticulated.txt").remove()

    def llamas_ass_kicked(self):
        assert self.path.state.joinpath("kicked_llamas_ass.txt").exists()
        self.path.state.joinpath("kicked_llamas_ass.txt").remove()

    def output_is(self, expected_contents):
        output_contents = self.path.state.joinpath("output.txt").bytes().decode('utf8').strip()
        regex = DefaultSimex(
            open_delimeter="(((",
            close_delimeter=")))",
            exact=True,
        ).compile(expected_contents.strip())
        if regex.match(output_contents) is None:
            raise RuntimeError("Expected output:\n{0}\n\nActual output:\n{1}".format(
                expected_contents,
                output_contents,
            ))
        self.path.state.joinpath("output.txt").remove()

    def output_contains(self, expected_contents):
        output_contents = self.path.state.joinpath("output.txt").bytes().decode('utf8').strip()
        regex = DefaultSimex(
            open_delimeter="(((",
            close_delimeter=")))",
        ).compile(expected_contents.strip())
        if regex.search(output_contents) is None:
            raise RuntimeError("Expected to find:\n{0}\n\nActual output:\n{1}".format(
                expected_contents,
                output_contents,
            ))
        self.path.state.joinpath("output.txt").remove()

    def output_will_be(self, reference, changeable=None):
        output_contents = self.path.state.joinpath("output.txt").bytes().decode('utf8').strip()

        artefact = self.path.engine.joinpath(
            "artefacts", "{0}.txt".format(reference.replace(" ", "-").lower())
        )

        simex = DefaultSimex(
            open_delimeter="(((",
            close_delimeter=")))",
        )

        simex_contents = output_contents

        if changeable is not None:
            for replacement in changeable:
                simex_contents = simex.compile(replacement).sub(replacement, simex_contents)

        if not artefact.exists():
            artefact.write_text(simex_contents)
        else:
            if self.settings.get('overwrite artefacts'):
                artefact.write_text(simex_contents)
                self.services.log(output_contents)
            else:
                if simex.compile(artefact.bytes().decode('utf8')).match(output_contents) is None:
                    raise RuntimeError("Expected to find:\n{0}\n\nActual output:\n{1}".format(
                        artefact.bytes().decode('utf8'),
                        output_contents,
                    ))
                else:
                    self.services.log(output_contents)

    def pause(self, message=""):
        if hasattr(self, 'services') and self.services is not None:
            self.services.start_interactive_mode()
        self.ipython(message=message)
        if hasattr(self, 'services') and self.services is not None:
            self.services.stop_interactive_mode()

    def on_failure(self):
        """Stop and IPython."""
        if self.settings.get("kaching", False):
            kaching.fail()
        if self.settings.get("pause_on_failure", True):
            self.services.log(message=self.stacktrace.to_template())
            self.shell()

    def on_success(self):
        """Ka-ching!"""
        if self.settings.get("kaching", False):
            kaching.win()
        if self.settings.get("pause_on_success", False):
            self.pause(message="SUCCESS")

    def shell(self):
        if hasattr(self, 'services'):
            self.services.start_interactive_mode()
            time.sleep(0.5)
            import sys
            if path.exists(path.join(
                path.expanduser("~"), ".ipython/profile_default/security/",
                self.ipython_kernel_filename)
            ):
                call([
                        sys.executable, "-m", "jupyter_console",
                        "--existing",
                        path.join(
                            path.expanduser("~"),
                            ".ipython/profile_default/security/",
                            self.ipython_kernel_filename
                        )
                    ])
            else:
                call([
                    sys.executable, "-m", "jupyter_console",
                    "--existing", self.ipython_kernel_filename
                ])
            self.services.stop_interactive_mode()

    def stop_services(self):
        if hasattr(self, 'services'):
            if self.services is not None:
                self.services.shutdown()

    def tear_down(self):
        """Clean out the state directory."""
        self.stop_services()
