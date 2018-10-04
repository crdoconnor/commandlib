No arguments:
  based on: commandlib
  given:
    scripts:
      outputtext: |
        #!/bin/bash
        echo hello > output
    setup: |
      from commandlib import Command
  steps:
  - Run: Command("./outputtext").run()
  - File contents will be:
      filename: output
      contents: hello


One argument:
  based on: commandlib
  given:
    scripts:
      outputtext: |
        #!/bin/bash
        echo hello $1 > output
    setup: |
      from commandlib import Command
  steps:
    - Run: Command("./outputtext", "mark").run()
    - File contents will be:
        filename: output
        contents: hello mark
