Ignore non-zero exit codes:
  based on: commandlib
  given:
    scripts:
      outputtext: |
        #!/bin/bash
        echo hello > output
        exit 1
    setup: from commandlib import Command
  steps:
    - Run: Command("./outputtext").ignore_errors().run()
    - File contents will be:
        filename: output
        contents: hello
