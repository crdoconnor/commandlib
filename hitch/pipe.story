Piping data in from string or file (.piped):
  docs: pipe-data-in
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
    from string:
      steps:
      - Run: |
          with open("person", "r") as handle:
              command_path.command1().piped.from_string("harry").run()

      - File contents will be:
          filename: output
          contents: hello harry
          
    from file handle:
      steps:
      - Run: |
          with open("person", "r") as handle:
              command_path.command1().piped.from_handle(handle).run()

      - File contents will be:
          filename: output
          contents: hello harry
    
    from filename:
      steps:
      - Run: |
          command_path.command1().piped.from_filename("person").run()

      - File contents will be:
          filename: output
          contents: hello harry


Piping data out to string or file (.piped):
  docs: pipe-data-out
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
    stdout to file handle:
      steps:
      - Run: |
          with open("regular", "w") as handle:
              command_path.command1("harry").piped.stdout_to_handle(handle).run()

      - File contents will be:
          filename: regular
          contents: hello harry

    stdout to filename:
      steps:
      - Run: |
          command_path.command1("harry").piped.stdout_to_filename("regular").run()

      - File contents will be:
          filename: regular
          contents: hello harry
          
    stderr to file handle:
      steps:
      - Run: |
          with open("error", "w") as handle:
              command_path.command2("tom").piped.stderr_to_handle(handle).run()

      - File contents will be:
          filename: error
          contents: hello tom
