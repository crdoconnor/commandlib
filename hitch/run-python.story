Use current python environment:
  about: |
    You can run python code in the same environment
    by importing "python" command object or the
    "python_bin" command path.
    
    If you are running the code in a virtualenv, for
    example, the python object will refer to the python
    binary in the virtualenv bin directory.
  based on: commandlib
  given:
    scripts:
      outputtext.py: |
        with open("output", "w") as handle:
            handle.write("hello")
    setup: |
      from commandlib import python, python_bin
  variations:
    Run python: 
      steps:
      - Run: python("outputtext.py").run()
      - File contents will be:
          filename: output
          contents: hello
  
    Use python_bin: 
      steps:
      - Run: python_bin.python("outputtext.py").run()
      - File contents will be:
          filename: output
          contents: hello
