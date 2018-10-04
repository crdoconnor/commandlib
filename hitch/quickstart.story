Quickstart:
  based on: commandlib
  given:
    scripts:
      django/manage.py: |
        import sys
        sys.stdout.write(' '.join(sys.argv[1:]))
    setup: |
      from commandlib import Command

      # Create base command
      python = Command("python")

      # Create sub-commands from base command
      manage = python("manage.py").in_dir("django")

      dev_manage = manage.with_trailing_args("--settings", "local_settings.py")
  steps:
  - Run:
      code: |
        # Run the command!
        dev_manage("runserver", "8080").run()
      will output: runserver 8080 --settings local_settings.py
