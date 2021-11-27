Run commmands interactively using icommandlib or pexpect:
  docs: run-interactively
  about: |
    However, if the command you want to run requires that:
    
    * It prompts the user for a response (yes or no / password / etc.)
    * It 'draws' on a terminal window - like 'top'.
    * You want to interact with the process and do other stuff while it runs
    (e.g. wait for a database service to warm up and then continue).
    
    Then you need an interactive library.
    
    Commandlib can call and create an interactive process object for two
    other libraries this way - [ICommandLib](https://github.com/crdoconnor/icommandlib)
    and [pexpect](https://pexpect.readthedocs.io/en/stable/).
    
    The two examples below are not actually interactive but they demonstrate
    how pexpect and icommandlib can be used.
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
      about: |
        NOTE: You need to "pip install icommandlib" to use this command
        or you will get an import error.
      fails_on_python_2: yes
      given:
        icommandlib version: 0.1.2
      steps:
      - Run: |
          process = Command("./outputtext", "mark").interactive().run()
          process.wait_until_output_contains("mark")
          process.wait_for_successful_exit()

    pexpect:
      about: |
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
