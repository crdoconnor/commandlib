from os.path import join, isfile, exists, abspath
from os import listdir, access
from commandlib.exceptions import CommandError
from commandlib.command import Command
import os


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
