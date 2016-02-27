import copy
from os import path, chdir, getcwd, listdir, access
from os.path import join, isfile, exists
from subprocess import call, PIPE
import os

class CommandError(Exception):
    pass


class Command(object):
    def __init__(
        self,
        arguments,
        directory=None,
        env=None,
        shell=False,
        trailing_args=None,
        paths=None
    ):
        """Create new command object."""
        if type(arguments) is not list:
            arguments = [str(arguments), ]
        self._arguments = [str(arg) for arg in arguments]
        self._directory = str(directory) if directory is not None else None
        self._env = dict(env) if env is not None else {}
        self._shell = bool(shell)
        self._paths = [str(path) for path in paths] if paths is not None else []
        self._trailing_args = [str(arg) for arg in trailing_args] \
            if trailing_args is not None else []
        self._silent_stdout = False
        self._silent_stderr = False
        self._ignore_errors = False

    @property
    def arguments(self):
        return self._arguments + self._trailing_args

    @property
    def env(self):
        env_vars = os.environ.copy()
        env_vars.update(self._env)
        new_path = ":".join(
            [env_vars["PATH"], ] if "PATH" in env_vars else [] + self._paths
        )
        env_vars["PATH"] = new_path
        return env_vars
    
    def ignore_errors(self):
        new_command = copy.deepcopy(self)
        new_command._ignore_errors = True
        return new_command

    @property
    def directory(self):
        return self._directory

    def __call__(self, *arguments):
        args = [str(arg) for arg in arguments]
        new_command = copy.deepcopy(self)
        new_command._arguments.extend(arguments)
        return new_command

    def with_env(self, **environment_variables):
        new_env_vars = {
            str(var): str(val) for var, val in environment_variables.items()
        }
        new_command = copy.deepcopy(self)
        new_command._env.update(new_env_vars)
        return new_command

    def in_dir(self, directory):
        new_command = copy.deepcopy(self)
        new_command._directory = str(directory)
        return new_command

    def with_shell(self):
        new_command = copy.deepcopy(self)
        new_command._shell = True
        return new_command

    def with_trailing_args(*arguments):
        new_command = copy.deepcopy(self)
        new_command._trailing_args = [str(arg) for arg in arguments]
        return new_command

    def with_path(self, path):
        new_command = copy.deepcopy(self)
        new_command._paths.append(str(path))
        return new_command

    def silently(self):
        new_command = copy.deepcopy(self)
        new_command._silent_stdout = True
        new_command._silent_stderr = True
        return new_command

    def only_errors(self):
        new_command = copy.deepcopy(self)
        new_command._silent_stdout = True
        new_command._silent_stderr = False
        return new_command

    def __str__(self):
        return " ".join(self.arguments)

    def __unicode__(self):
        return " ".join(self.arguments)

    def __repr__(self):
        return self.__str__()



class Commands(object):
    def __init__(self, bin_directory=None):
        self.bin_directory = bin_directory

        if bin_directory is not None:
            for filename in listdir(bin_directory):
                absfilename = join(bin_directory, filename)
                
                if isfile(absfilename) and access(absfilename, os.X_OK):
                    setattr(
                        self,
                        filename.replace(".", "_").replace("-", "_"),
                        Command(absfilename, paths=[bin_directory, ])
                    )

    def __setattr__(self, name, value):
        if type(value) != Command:
            raise CommandError("Command must be of type commandlib.Command")
        self.__dict__[name] = value



def run(command):
    """Run Command object."""
    if type(command) != Command:
        raise CommandError("Command must be of type commandlib.Command")

    previous_directory = getcwd()

    if command.directory is not None:
        if not exists(command.directory):
            raise CommandError(
                "Cannot run {0} - directory {0} does not exist".format(
                    command.__repr__(), directory
                )
            )
        chdir(command.directory)

    returncode = call(
        command.arguments,
        env=command.env,
        shell=command._shell,
        stdout=PIPE if command._silent_stdout else None,
        stderr=PIPE if command._silent_stderr else None,
    )
    
    chdir(previous_directory)

    if returncode != 0 and not command._ignore_errors:
        raise CommandError('"{0}" failed (err code {1})'.format(
            command.__repr__(),
            returncode
        ))
