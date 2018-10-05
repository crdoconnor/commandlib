Setting PATH does not overwrite other environment variables:
  based on: commandlib
  given:
    scripts:
      outputtext: |
        #!/bin/bash
        echo hello $ENVVAR > output
    setup: from commandlib import Command
  steps:
  - Run: Command("outputtext").with_env(ENVVAR="harry").with_path(".").run()
  - File contents will be:
      filename: output
      contents: hello harry
