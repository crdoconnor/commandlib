from subprocess import check_call, call, PIPE, CalledProcessError
from os import path, system, chdir
import hitchpython
import hitchserve
import hitchtest
import hitchcli
import signal


# Get directory above this file
PROJECT_DIRECTORY = path.abspath(path.join(path.dirname(__file__), '..'))

class ExecutionEngine(hitchtest.ExecutionEngine):
    """Python engine for running tests."""

    def set_up(self):
        """Set up your applications and the test environment."""
        chdir(PROJECT_DIRECTORY)
        self.python_package = hitchpython.PythonPackage(
            self.preconditions.get('python_version', '3.5.0')
        )
        self.python_package.build()

        # Uninstall and reinstall
        call([self.python_package.pip, "install", "ipython==1.2.1", ], stdout=PIPE)
        call([self.python_package.pip, "install", "pyzmq", ], stdout=PIPE)
        call([self.python_package.pip, "uninstall", "commandlib", "-y"], stdout=PIPE)
        check_call([self.python_package.python, "setup.py", "install"], stdout=PIPE)
        
        self.services = hitchserve.ServiceBundle(
            PROJECT_DIRECTORY,
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

    def on_failure(self):
        if self.settings.get("pause_on_failure", True):
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


    def flake8(self, directory):
        # Silently install flake8
        check_call([self.python_package.pip, "install", "flake8"], stdout=PIPE)
        try:
            check_call([
                path.join(self.python_package.bin_directory, "flake8"),
                directory
            ])
        except CalledProcessError:
            raise RuntimeError("flake8 failure")

    def run_unit_tests(self, directory):
        chdir(PROJECT_DIRECTORY)
        try:
            check_call([
                path.join(self.python_package.bin_directory, "py.test"),
                "--maxfail=1",
                "-s",
                directory
            ])
        except CalledProcessError:
            raise RuntimeError("py.test failure")

    def tear_down(self):
        if hasattr(self, 'services'):
            self.services.shutdown()
        try:
            self.end_python_interpreter()
        except:
            pass
