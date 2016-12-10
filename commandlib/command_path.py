from os.path import join, isfile, exists, abspath
from os import listdir, access
from commandlib.exceptions import CommandError
from commandlib.command import Command
import os


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
                "Can't create CommandPath object: {0} does not exist.".format(
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
