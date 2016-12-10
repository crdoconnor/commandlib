from subprocess import check_call, call, PIPE, CalledProcessError
from os import path, system, chdir
from commandlib import run, CommandError
import hitchpython
import hitchserve
import hitchtest
import hitchcli
import signal


# Get directory above this file
#PROJECT_DIRECTORY = path.abspath(path.join(path.dirname(__file__), '..'))

class ExecutionEngine(hitchtest.ExecutionEngine):
    """Python engine for running tests."""

    def set_up(self):
        """Set up your applications and the test environment."""
        self.path.project = self.path.engine.parent

        if self.path.state.exists():
            self.path.state.rmtree(ignore_errors=True)
        self.path.state.mkdir()

        for script, text in self.preconditions.get("scripts", {}).items():
            script_file = self.path.state.joinpath(script)
            if not script_file.dirname().exists():
                script_file.dirname().mkdir()
            script_file.write_text(text)
            script_file.chmod("u+x")

        self.python_package = hitchpython.PythonPackage(
            self.preconditions.get('python_version', '3.5.0')
        )
        self.python_package.build()

        self.pip = self.python_package.cmd.pip
        self.python = self.python_package.cmd.python

        # Uninstall and reinstall
        run(self.pip("install", "flake8"))
        run(self.pip("install", "ipython==1.2.1").ignore_errors())
        run(self.pip("install", "pyzmq").ignore_errors())
        run(self.pip("uninstall", "commandlib", "-y").ignore_errors())
        run(self.pip("install", ".").in_dir(self.path.project))

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
        self.run_command("from commandlib import Command, run")
        self.run_command("import os")
        self.run_command("os.chdir('{}')".format(self.path.state))

    def on_failure(self):
        if self.settings.get("pause_on_failure", True):
            if self.preconditions.get("launch_shell", True):
                if hasattr(self, 'services'):
                    import sys
                    self.services.log(message=self.stacktrace.to_template())
                    self.services.start_interactive_mode()
                    if path.exists(path.join(
                        path.expanduser("~"), ".ipython/profile_default/security/",
                        self.ipython_kernel_filename)
                    ):
                        call([
                                sys.executable, "-m", "IPython", "console",
                                "--existing",
                                path.join(
                                    path.expanduser("~"),
                                    ".ipython/profile_default/security/",
                                    self.ipython_kernel_filename
                                )
                            ])
                    else:
                        call([
                            sys.executable, "-m", "IPython", "console",
                            "--existing", self.ipython_kernel_filename
                        ])
                    self.services.stop_interactive_mode()

    def assert_file_contains(self, filename, contents):
        assert self.path.state.joinpath(filename).bytes().decode('utf8').strip() == contents.strip()

    def flake8(self, directory, args=None):
        # Silently install flake8
        self.services.start_interactive_mode()
        flake8 = self.python_package.cmd.flake8
        try:
            run(flake8(str(self.path.project.joinpath(directory)), *args).in_dir(self.path.project))
        except CommandError:
            raise RuntimeError("flake8 failure")

    def pause(self, message="Pause"):
        if hasattr(self, 'services'):
            self.services.start_interactive_mode()
        self.ipython(message)
        if hasattr(self, 'services'):
            self.services.stop_interactive_mode()


    def tear_down(self):
        if hasattr(self, 'services'):
            self.services.shutdown()
        try:
            self.end_python_interpreter()
        except:
            pass
