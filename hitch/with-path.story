Add directory to PATH (with_path):
  docs: add-directory-to-path
  based on: commandlib
  about: |
    If you want to run a command with an additional folder on
    the path you can specify it with with_path.

    Note that if you use [CommandPath](../command-path) object,
    the directory you use it on is already added.
  given:
    scripts:
      bin_directory/ls: |
        #!/bin/bash
        echo hello $1 > output
      runls: |
        #!/bin/bash
        ls $1
    setup: |
      from commandlib import Command

      runls = Command("./runls")
  variations:
    Add bin_directory to PATH for runls:
      steps:
      - Run: runls("harry").with_path("bin_directory").run()
      - File contents will be:
          filename: output
          contents: hello harry
