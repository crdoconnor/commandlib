import copy
from os import path, chdir, getcwd, listdir, access
from os.path import join, isfile, exists, abspath
from subprocess import call, PIPE
import os

class CommandError(Exception):
    """commandlib exception."""
    pass


class Command(object):
    """
    Command object containing details of a command and how it should be run.
    
    Including:
      * Command and arguments.
      * Directory to run the command in.
      * PATH to run the command with (on top of system paths).
      * Environment variables to run with the command.
    """
    def __init__(
        self,
        arguments,
        directory=None,
        env=None,
        shell=False,
        trailing_args=None,
        paths=None
    ):
        """
        Create new command object.
        
        Args:
            arguments (List(str)): Sequence of program arguments needed to run the service.
            directory (Optional[str/Path object]): Directory to run the command in.
            env (Optional[dict]): Additional environment variables to feed to the command.
            shell (Optional[bool]): Run the command using shell or not? (default: False).
            trailing_args (Optional[List[str]]): Trailing arguments to run the command with (default: None).
            paths (Optional[List[str/Path]]): Additions to the PATH for this command (default: None).
        """
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
        args = [str(arg) for arg in arguments]
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

    def in_dir(self, directory):
        """
        Return new Command object that will be run in specified
        directory.
        """
        
        # TODO : Check directory's existence before continuing.
        
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

    def with_trailing_args(*arguments):
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

    def __str__(self):
        return " ".join(self.arguments)

    def __unicode__(self):
        return " ".join(self.arguments)

    def __repr__(self):
        return self.__str__()



class Commands(object):
    """
    Command group object representing a group of executable commands.
    """
    def _directory_commands(self):
        commands = {}
        
        if self.bin_directory is not None:
            for filename in listdir(self.bin_directory):
                absfilename = join(self.bin_directory, filename)
                
                if isfile(absfilename) and access(absfilename, os.X_OK):
                    object_name = filename.replace(".", "_").replace("-", "_")
                    commands[object_name] = Command(
                        absfilename, paths=[self.bin_directory, ]
                    )
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
                set(self._added_commands.keys()) |\
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
