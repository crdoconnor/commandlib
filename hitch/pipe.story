Pipe in:
  based on: commandlib
  given:
    scripts:
      bin_directory/command1: |
        #!/bin/bash
        read X
        echo hello $X > output
    files:
      person: harry
    setup: |
      from commandlib import CommandPath
      command_path = CommandPath("./bin_directory")
  variations:
    from file:
      steps:
      - Run: |
          with open("person", "r") as handle:
              command_path.command1().piped.from_handle(handle).run()

      - File contents will be:
          filename: output
          contents: hello harry
    
    from string:
      steps:
      - Run: |
          with open("person", "r") as handle:
              command_path.command1().piped.from_string("harry").run()

      - File contents will be:
          filename: output
          contents: hello harry


Pipe out:
  based on: commandlib
  given:
    scripts:
      bin_directory/command1: |
        #!/bin/bash
        echo hello $1
      bin_directory/command2: |
        #!/bin/bash
        echo hello $1 1>&2
    setup: |
      from commandlib import CommandPath
      command_path = CommandPath("./bin_directory")
  variations:
    stdout to file:
      steps:
      - Run: |
          with open("regular", "w") as handle:
              command_path.command1("harry").piped.stdout_to_handle(handle).run()

      - File contents will be:
          filename: regular
          contents: hello harry
          
    stderr to file:
      steps:
      - Run: |
          with open("error", "w") as handle:
              command_path.command2("tom").piped.stderr_to_handle(handle).run()

      - File contents will be:
          filename: error
          contents: hello tom
