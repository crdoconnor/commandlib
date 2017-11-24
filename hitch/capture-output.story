Capture output from stdout:
  based on: commandlib
  description: |
    You can run a command and capture the stdout to a string
    using .output().

    This is unsuitable for:

    * Capturing output from stderr.
    * Capturing output from programs that draw all over the screen (like top).
    * Capturing output from programs that output special terminal characters (e.g. color characters)
    * Capturing output from programs mid-run.
    * Interacting with programs that use user input.
    
    For all of the above use cases and more, use icommandlib.
  given:
    scripts:
      outputtext: |
        #!/bin/bash
        echo hello
      raiseerror: |
        #!/bin/bash
        echo bad output
        exit 1
    setup: from commandlib import Command
  variations:
    Success:
      steps:
      - Run: assert Command("./outputtext").output().strip() == "hello"

    Error:
      steps:
      - Run:
          code: Command("./raiseerror").output().strip()
          raises:
            type: commandlib.exceptions.CommandExitError
            message: "\"./raiseerror\" failed (err code 1), stdout:\n\nbad output\n\
              \n\nstderr:\n\n"
