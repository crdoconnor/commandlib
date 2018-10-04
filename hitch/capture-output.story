Capture output:
  docs: capture-output
  based on: commandlib
  about: |
    You can run a command and capture the stdout and stderr to a string
    using .output().

    This is unsuitable for:

    * Capturing output from programs that draw all over the screen (like top).
    * Capturing output from programs that output special terminal characters (e.g. color characters).
    * Interacting with programs that use user input.
    
    For all of the above use cases and more, command.interact() is more suitable.
  given:
    scripts:
      outputtext: |
        #!/bin/bash
        echo hello from stdout
        >&2 echo "hello from stderr"
      raiseerror: |
        #!/bin/bash
        echo bad output from stdout
        >&2 echo "bad output from stderr"
        exit 1
    setup: from commandlib import Command
  variations:
    Success:
      steps:
      - Run: |
          assert Command("./outputtext").output().strip() \
            == "hello from stdout\nhello from stderr"

    Error:
      steps:
      - Run:
          code: Command("./raiseerror").output().strip()
          raises:
            type: commandlib.exceptions.CommandExitError
            message: |-
              "./raiseerror" failed (err code 1), output:
              
              bad output from stdout
              bad output from stderr
