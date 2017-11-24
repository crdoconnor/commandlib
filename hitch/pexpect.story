Run pexpect and get process:
  based on: commandlib
  given:
    pexpect version: 4.2.1
    scripts:
      outputtext: |
        #!/bin/bash
        echo hello $1
    setup: |
      from commandlib import Command
      from pexpect import EOF
  steps:
    - Run: |
       process = Command("./outputtext", "mark").pexpect()
       process.expect("mark")
       process.expect(EOF)
       process.close()
