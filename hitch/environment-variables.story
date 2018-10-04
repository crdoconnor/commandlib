Run with extra environment variables:
  docs: environment-variables
  based on: commandlib
  about: |
    Environment variables can be set and passed down
    to commands or, alternative, environment variables can
    be explicitly dropped.

    All parent environment variables will be passed on by
    default.
  given:
    scripts:
      outputtext: |
        #!/bin/bash
        echo hello $ENVVAR > output
      outputpath: |
        #!/bin/bash
        echo hello $HOME > output
    setup: |
      from commandlib import Command
  variations:
    With extra environment variable:
      steps:
      - Run: Command("./outputtext").with_env(ENVVAR="tom").run()
      - File contents will be:
          filename: output
          contents: hello tom
    
    Dropping an environment variable:
      steps:
      - Run: Command("./outputpath").without_env("HOME").run()
      - File contents will be:
          filename: output
          contents: hello

