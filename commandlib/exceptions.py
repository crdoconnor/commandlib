class CommandError(Exception):
    """commandlib exception."""
    pass


class CommandExitError(CommandError):
    def __init__(self, command_repr, return_code, stdout=None, stderr=None):
        self.command_repr = command_repr
        self.return_code = return_code
        self.stdout = stdout
        self.stderr = stderr

    def __unicode__(self):
        return '"{0}" failed (err code {1}), stdout:\n\n{2}\n\nstderr:\n\n{3}'.format(
            self.command_repr,
            self.return_code,
            self.stdout,
            self.stderr,
        )

    def __str__(self):
        return self.__unicode__()

    def __repr__(self):
        return self.__str__()
