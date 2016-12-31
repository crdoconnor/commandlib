from os import chdir, getcwd
from subprocess import call, PIPE
from commandlib.utils import _check_directory
from commandlib.exceptions import CommandError
import io
import copy
import os


def _type_check_command(command):
    """Raise exception if non-Command object passed."""
    if type(command) != Command:
        raise CommandError("Command must be of type commandlib.Command")


def run(command):
    """Run Command object."""
    _type_check_command(command)
    command.run()


class Command(object):
    """
    Command object containing details of a command and how it should be run.

    Including:
      * Command and arguments.
      * Directory to run the command in.
      * PATH to run the command with (on top of system paths).
      * Environment variables to run with the command.
    """
    def __init__(self, *args):
        """
        Create new command object::

            Command("docommand", "argument1", "argument2")
        """
        self._arguments = [str(arg) for arg in args]
        self._directory = None
        self._env = {}
        self._env_drop = []
        self._shell = None
        self._paths = []
        self._trailing_args = []
        self._silent_stdout = False
        self._silent_stderr = False
        self._ignore_errors = False
        self._pipe_stdout_to_file = None
        self._pipe_stderr_to_file = None
        self._pipe_from_file = None

    @property
    def arguments(self):
        """
        Return a full list of the arguments that this command will be run with.
        """
        return self._arguments + self._trailing_args

    @property
    def env(self):
        """
        Dict of all environment variables that will be run with this command.
        """
        env_vars = os.environ.copy()
        env_vars.update(self._env)
        new_path = ":".join(
            [env_vars["PATH"], ] + self._paths if "PATH" in env_vars else [] + self._paths
        )
        env_vars["PATH"] = new_path
        for env_var in self._env_drop:
            if env_var in env_vars:
                del env_vars[env_var]
        return env_vars

    def ignore_errors(self):
        """
        Return new command object that will not raise an exception when
        return code > 0.
        """
        new_command = copy.deepcopy(self)
        new_command._ignore_errors = True
        return new_command

    @property
    def directory(self):
        """
        Return directory that this command will be run in.

        If None, then the command will be run in the current directory.
        """
        return self._directory

    def __call__(self, *arguments):
        """
        When the Command object is called, it returns a new Command
        object with additional arguments.
        """
        arguments = [str(arg) for arg in arguments]     # Force list to string
        new_command = copy.deepcopy(self)
        new_command._arguments.extend(arguments)
        return new_command

    def with_env(self, **environment_variables):
        """
        Return new Command object that will be run with additional
        environment variables.

        Specify environment variables as follows:

            new_cmd = old_cmd.with_env(PYTHON_PATH=".", ENV_PORT="2022")
        """
        new_env_vars = {
            str(var): str(val) for var, val in environment_variables.items()
        }
        new_command = copy.deepcopy(self)
        new_command._env.update(new_env_vars)
        return new_command

    def without_env(self, environment_variable):
        """
        Return new Command object that will drop a specified
        environment variable if it is set.

            new_cmd = old_cmd.without_env("PYTHON_PATH")
        """
        new_command = copy.deepcopy(self)
        new_command._env_drop.append(str(environment_variable))
        return new_command

    def in_dir(self, directory):
        """
        Return new Command object that will be run in specified
        directory.

            new_cmd = old_cmd.in_dir("/usr")
        """
        new_command = copy.deepcopy(self)
        new_command._directory = str(directory)
        return new_command

    def with_shell(self):
        """
        Return new Command object that will be run using shell.
        """
        new_command = copy.deepcopy(self)
        new_command._shell = True
        return new_command

    def with_trailing_args(self, *arguments):
        """
        Return new Command object that will be run with specified
        trailing arguments.
        """
        new_command = copy.deepcopy(self)
        new_command._trailing_args = [str(arg) for arg in arguments]
        return new_command

    def with_path(self, path):
        """
        Return new Command object that will be run with a new addition
        to the PATH environment variable that will be fed to the command.
        """
        new_command = copy.deepcopy(self)
        new_command._paths.append(str(path))
        return new_command

    def silently(self):
        """
        Return new Command object that will be run with stdout and
        stderr suppressed.
        """
        new_command = copy.deepcopy(self)
        new_command._silent_stdout = True
        new_command._silent_stderr = True
        return new_command

    def only_errors(self):
        """
        Return new Command object that will be run with stdout but
        not stderr suppressed.
        """
        new_command = copy.deepcopy(self)
        new_command._silent_stdout = True
        new_command._silent_stderr = False
        return new_command

    def pipe_stdout_to_file(self, handle):
        """
        Pipe the stdout output to file handle 'handle'.

        Example usage::
          command.pipe_stdout_to_file(open("/tmp/output", 'w'))
        """
        new_command = copy.deepcopy(self)
        new_command._pipe_stdout_to_file = handle
        return new_command

    def pipe_stderr_to_file(self, handle):
        """
        Pipe the stderr output to file handle 'handle'.

        Example usage::
          command.pipe_stderr_to_file(open("/tmp/output", 'w'))
        """
        new_command = copy.deepcopy(self)
        new_command._pipe_stderr_to_file = handle
        return new_command

    def pipe_from_file(self, handle):
        """
        Pipe the stderr output to file handle 'handle'.

        Example usage::
          command.pipe_stderr_to_file(open("/tmp/output", 'w'))
        """
        new_command = copy.deepcopy(self)
        new_command._pipe_from_file = handle
        return new_command

    def pexpect(self):
        """
        Run command and return pexpect process object.
        """
        import pexpect
        assert self._pipe_stderr_to_file is None
        assert self._pipe_stdout_to_file is None
        assert self._pipe_from_file is None
        assert self._silent_stdout == False
        assert self._silent_stderr == False
        assert self._ignore_errors == False

        _check_directory(self.directory)

        previous_directory = getcwd()

        if self.directory is not None:
            chdir(self.directory)

        arguments = self.arguments

        return pexpect.spawn(
            arguments[0],
            args=arguments[1:],
            env=self.env
        )

        chdir(previous_directory)

    def run(self):
        """Run command and wait until it finishes."""
        _check_directory(self.directory)

        previous_directory = getcwd()

        if self.directory is not None:
            chdir(self.directory)

        stdout = None

        if self._pipe_stdout_to_file is not None:
            stdout = self._pipe_stdout_to_file

        if self._silent_stdout:
            stdout = PIPE

        stderr = None

        if self._pipe_stderr_to_file is not None:
            stderr = self._pipe_stderr_to_file

        if self._silent_stderr:
            stderr = PIPE

        stdin = None if self._pipe_from_file is None else self._pipe_from_file

        returncode = call(
            self.arguments,
            env=self.env,
            shell=self._shell,
            stdout=stdout,
            stderr=stderr,
            stdin=stdin,
        )

        chdir(previous_directory)

        if returncode != 0 and not self._ignore_errors:
            raise CommandError('"{0}" failed (err code {1})'.format(
                self.__repr__(),
                returncode
            ))

    def __str__(self):
        return " ".join(self.arguments)

    def __unicode__(self):
        return " ".join(self.arguments)

    def __repr__(self):
        return self.__str__()
