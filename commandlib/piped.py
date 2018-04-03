from copy import deepcopy
from subprocess import PIPE, STDOUT, Popen
from commandlib.exceptions import CommandError, CommandExitError
from commandlib.utils import _check_directory
from os import chdir, getcwd


class PipedCommand(object):
    def __init__(self, command):
        self._command = command
        self._from_string = None
        self._from_handle = None
        self._stdout_to_handle = None
        self._stderr_to_handle = None

    def from_string(self, string):
        assert self._from_handle is None
        new_piped = deepcopy(self)
        new_piped._from_string = string
        return new_piped

    def from_handle(self, handle):
        assert self._from_string is None
        new_piped = deepcopy(self)
        new_piped._from_handle = handle
        return new_piped

    def stdout_to_handle(self, handle):
        new_piped = deepcopy(self)
        new_piped._stdout_to_handle = handle
        return new_piped

    def stderr_to_handle(self, handle):
        assert self._stderr_to_handle is None
        new_piped = deepcopy(self)
        new_piped._stderr_to_handle = handle
        return new_piped

    def run(self):
        _check_directory(self._command.directory)

        previous_directory = getcwd()

        if self._from_handle is None and self._from_string is None:
            stdin = None
        else:
            if self._from_string:
                stdin = PIPE
            if self._from_handle:
                stdin = self._from_handle

        if self._stdout_to_handle is None:
            stdout = None
        else:
            if self._stdout_to_handle:
                stdout = self._stdout_to_handle

        if self._stderr_to_handle is None:
            stderr = PIPE
        else:
            if self._stderr_to_handle:
                stderr = self._stderr_to_handle

        if self._command.directory is not None:
            chdir(self._command.directory)

        process = Popen(
            self._command.arguments,
            stdout=stdout,
            stderr=stderr,
            stdin=stdin,
            shell=self._command._shell,
            env=self._command.env,
        )

        if self._from_string:
            process.stdin.write(self._from_string.encode('utf8'))

        _, _ = process.communicate()

        returncode = process.returncode

        chdir(previous_directory)

        if returncode != 0 and not self._command._ignore_errors:
            raise CommandError('"{0}" failed (err code {1})'.format(
                self.__repr__(),
                returncode
            ))

    def output(self):
        _check_directory(self._command.directory)

        previous_directory = getcwd()

        if self._command.directory is not None:
            chdir(self._command.directory)

        if self._from_handle is None and self._from_string is None:
            stdin = None
        else:
            if self._from_string:
                stdin = PIPE
            if self._from_handle:
                stdin = self._from_handle

        process = Popen(
            self._command.arguments,
            stdout=PIPE,
            stderr=STDOUT,
            stdin=stdin,
            shell=self._command._shell,
            env=self._command.env,
        )

        if self._from_string:
            process.stdin.write(self._from_string.encode('utf8'))

        stdoutput, _ = process.communicate()

        returncode = process.returncode

        chdir(previous_directory)

        if returncode != 0 and not self._command._ignore_errors:
            raise CommandExitError(
                self.__repr__(),
                returncode,
                stdoutput.decode('utf8').strip(),
            )

        return stdoutput.decode('utf8')

    def __str__(self):
        return " ".join(self._command.arguments)

    def __unicode__(self):
        return " ".join(self._command.arguments)

    def __repr__(self):
        return self.__str__()
