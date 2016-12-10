from commandlib.exceptions import CommandError
from os.path import exists, isdir


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
