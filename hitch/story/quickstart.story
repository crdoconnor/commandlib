Quickstart:
  based on: commandlib
  given:
    scripts:
      django/manage.py: |
        # Pretend django "manage.py" that just prints out arguments:
        import sys ; sys.stdout.write(' '.join(sys.argv[1:]))
    setup: |
      from commandlib import Command

      # Create base command
      python = Command("/usr/bin/python3")

      # Create command "python manage.py" that runs in the django directory
      manage = python("manage.py").in_dir("django")

      # Build even more specific command
      dev_manage = manage.with_trailing_args("--settings", "local_settings.py")
  steps:
  - Run:
      code: |
        # Run combined command
        dev_manage("runserver", "8080").run()
      will output: runserver 8080 --settings local_settings.py
