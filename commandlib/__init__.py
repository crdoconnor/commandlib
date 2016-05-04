from os import chdir, getcwd, listdir, access
from os.path import join, isfile, exists, abspath, isdir
from subprocess import call, PIPE
import copy
import os


class CommandError(Exception):
    """commandlib exception."""
    pass


def _type_check_command(command):
    """Raise exception if non-Command object passed."""
    if type(command) != Command:
        raise CommandError("Command must be of type commandlib.Command")


def _check_directory(directory):
    """Raise exception if directory does not exist."""
    if directory is not None:
        if not exists(directory):
            raise CommandError(
                "Cannot run command - directory {0} does not exist".format(
                    directory
                )
            )

        if not isdir(directory):
            raise CommandError(
                "Cannot run command - specified directory {0} is not a directory.".format(
                    directory
                )
            )


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

    def run(self):
        """Run command and wait until it finishes."""
        _check_directory(self.directory)

        previous_directory = getcwd()

        if self.directory is not None:
            chdir(self.directory)

        returncode = call(
            self.arguments,
            env=self.env,
            shell=self._shell,
            stdout=PIPE if self._silent_stdout else None,
            stderr=PIPE if self._silent_stderr else None,
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


class CommandPath(object):
    """
    Command group object representing a group of executable commands in a directory.
    """

    def __init__(self, directory):
        """
        Initialize a group of commands in the directory specified.

        Each of those commands will also be run with the directory added to the PATH
        environment variable.

        Commands can also be added to the object at any time.
        """
        directory = abspath(str(directory))

        if not exists(directory):
            raise CommandError(
                "Can't create Commands object: {0} does not exist.".format(
                    directory
                )
            )

        self._directory = directory

    def __getattr__(self, name):
        commands = {}

        for filename in listdir(self._directory):
            absfilename = join(self._directory, filename)

            if isfile(absfilename) and access(absfilename, os.X_OK):
                object_name = filename.replace(".", "_").replace("-", "_")
                commands[object_name] = Command(absfilename).with_path(self._directory)

        if name == "__methods__":
            return list(commands.keys())

        if name in commands:
            return commands[name]
        else:
            raise CommandError("'{0}' not found in '{1}'".format(name, self._directory))


class Commands(object):
    """
    Command group object representing a group of executable commands (DEPRECATED).
    """
    def _directory_commands(self):
        commands = {}

        if self.bin_directory is not None:
            for filename in listdir(self.bin_directory):
                absfilename = join(self.bin_directory, filename)

                if isfile(absfilename) and access(absfilename, os.X_OK):
                    object_name = filename.replace(".", "_").replace("-", "_")
                    commands[object_name] = Command(absfilename).with_path(self.bin_directory)
        return commands

    def __init__(self, bin_directory=None):
        """
        Initialize a group of commands.

        If bin_directory is specified, a dynamically updated command group from the
        list of commands in the specified directory will be created.

        Each of those commands will also be run with the directory added to the PATH
        environment variable.

        Commands can also be added to the object at any time.
        """
        if bin_directory is not None:
            bin_directory = abspath(str(bin_directory))

            if not exists(bin_directory):
                raise CommandError(
                    "Can't create Commands object: {0} does not exist.".format(
                        bin_directory
                    )
                )

        self.bin_directory = bin_directory
        self._added_commands = {}

    def __setattr__(self, name, value):
        if name in ["bin_directory", "_added_commands", ]:
            self.__dict__[name] = value
            return

        if type(value) != Command:
            raise CommandError(
                "Command {0} must be of type commandlib.Command".format(value.__repr__())
            )
        self._added_commands[name] = value

    def __getattr__(self, name):
        # Make tab autocompletion work in IPython
        if name in ["bin_directory", "_added_commands", ]:
            return self.__dict__[name]

        if name == "__methods__":
            return None

        if name == "trait_names" or name == "_getAttributeNames":
            return list(
                set(self._added_commands.keys()) |
                set(self._directory_commands().keys())
            )

        # If command is in _added_commands use that first
        if name in self._added_commands:
            return self._added_commands[name]

        dir_cmds = self._directory_commands()
        if name in dir_cmds.keys():
            return dir_cmds[name]

        raise CommandError("Command {0} not found in {1} or added commands: {2}".format(
            name,
            abspath(self.bin_directory),
            str(self._added_commands)
        ))


def run(command):
    """Run Command object."""
    _type_check_command(command)
    command.run()