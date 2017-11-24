Environment variables:
  based on: commandlib
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
    With:
      steps:
      - Run: Command("./outputtext").with_env(ENVVAR="tom").run()
      - File contents will be:
          filename: output
          contents: hello tom
    
    Drop:
      steps:
      - Run: Command("./outputpath").without_env("HOME").run()
      - File contents will be:
          filename: output
          contents: hello

