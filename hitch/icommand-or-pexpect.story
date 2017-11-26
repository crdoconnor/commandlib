Run interactively:
  description: |
    Commandlib is a small, self-contained library for running
    commands in the current terminal.
    
    If you want to use it a manner similar to the UNIX command
    line and pipe in to stdin via a string/file or pipe out
    stdout/stderr to a file/string you can.
    
    However, if the command you want to run requires that you
    run it in a more sophisticated way, for example:
    
    * It prompts the user for a response (yes or no / password / etc.)
    * It 'draws' on a terminal window - like 'top'.
    * You want to interact with the process and do other stuff while it runs (e.g. a database service)
    
    Then you need a more sophisticated library that can handle
    these kinds of interactions.
    
    Commandlib can call and create a process object for two
    other libraries this way - ICommandLib and pexpect.
    
    ICommandLib is currently in alpha and has some kinks,
    but should be a better replacement for pexpect soon.
    It only runs in python 3.
    
    Pexpect is very mature and runs in python 2 but is a bit
    long in the tooth.
  based on: commandlib
  given:
    scripts:
      outputtext: |
        #!/bin/bash
        echo hello $1
    setup: |
      from commandlib import Command
  variations:
    icommandlib:
      description: |
        NOTE: You need to "pip install icommandlib" to use this command
        or you will get an import error.
      fails on python 2: yes
      given:
        icommandlib version: 0.1.2
      steps:
      - Run: |
          process = Command("./outputtext", "mark").interactive().run()
          process.wait_until_output_contains("mark")
          process.wait_for_successful_exit()

    pexpect:
      description: |
        NOTE: You need to "pip install pexpect" to use this command
        or you will get an import error.
      given:
        pexpect version: 4.2.1
      steps:
      - Run: |
          from pexpect import EOF
          process = Command("./outputtext", "mark").pexpect()
          process.expect("mark")
          process.expect(EOF)
          process.close()