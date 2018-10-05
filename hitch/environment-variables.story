Change your command's environment variables (with_env):
  docs: environment-variables
  based on: commandlib
  about: |
    Environment variables can be set and passed down
    to commands or, alternative, environment variables can
    be explicitly dropped.

    All parent environment variables will be passed on by
    default.
  given:
    setup: |
      from commandlib import Command
  variations:
    With extra environment variable:
      given:
        scripts:
          outputtext: |
            #!/bin/bash
            echo hello $ENVVAR
      steps:
      - Run:
         code: Command("./outputtext").with_env(ENVVAR="tom").run()
         will output: hello tom

    Dropping an environment variable:
      given:
        scripts:
          outputpath: |
            #!/bin/bash
            echo hello $HOME
      steps:
      - Run:
          code: Command("./outputpath").without_env("HOME").run()
          will output: hello

    Dropping nonexistent variable does nothing:
      given:
        scripts:
          outputtext: |
            #!/bin/bash
            echo hello $SOMEOTHERVAR
      steps:
      - Run:
          code: Command("outputtext").without_env("NONEXISTENTVAR").with_path(".").run()
          will output: hello
