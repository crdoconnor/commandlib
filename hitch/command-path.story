Command Path:
  based on: commandlib
  description: |
    A CommandPath is an object that you can create to represent
    a directory with executables in it. You can then use that object
    to get command objects which you can then run.

    Command objects that are created from CommandPath objects 
    will automatically be run with that directory added to the beginning
    of their PATH. This means that they can run each other directly
    without specifying the directory.

    This feature was created to be able to create a "postgres" or "node"
    or "virtualenv" CommandPath object referencing their bin directory.
    Commands in those bin directories (e.g. python) could be run and
    be able to directly call other commands in that directory without
    referencing the absolute path.
  given:
    scripts:
      bin_directory/ls: |
        #!/bin/bash
        echo hello $1 > output
      bin_directory/command1: |
        #!/bin/bash
        ls $1
      bin_directory/command2: |
        #!/bin/bash
        echo hello $1 > output
      bin_directory/command_calling_command_in_path: |
        #!/bin/bash
        command1 tom
      bin_directory/command.with.dots: |
        #!/bin/bash
        echo hello dots > output
    setup: |
      from commandlib import CommandPath

      command_path = CommandPath("./bin_directory")
  variations:
    Run command from CommandPath:
      steps:
      - Run: command_path.command1("harry").run()
      - File contents will be:
          filename: output
          contents: hello harry

    Command can call other command in CommandPath without specifying its path:
      steps:
      - Run: command_path.command_calling_command_in_path("tom").run()
      - File contents will be:
          filename: output
          contents: hello tom

    Commands with dots in command path are translated into underscores:
      steps:
      - Run: command_path.command_with_dots("tom").run()
      - File contents will be:
          filename: output
          contents: hello dots

    Referencing a non-existent command raises an exception:
      steps:
      - Run:
          code: command_path.non_existent_command
          raises:
            type: commandlib.exceptions.CommandError
            message: "'non_existent_command' not found in '/home/colm/.hitch/qqxe6h/state/bin_directory'"
