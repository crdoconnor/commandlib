Environment var bugs:
  based on: Environment variables
  variations:
    Setting PATH does not overwrite other environment variables:
      steps:
      - Run: Command("outputtext").with_env(ENVVAR="harry").with_path(".").run()
      - File contents will be:
          filename: output
          contents: hello harry
    
    Dropping nonexistent variable does nothing:
      steps:
      - Run: Command("outputtext").without_env("NONEXISTENTVAR").with_path(".").run()
      - File contents will be:
          filename: output
          contents: hello
