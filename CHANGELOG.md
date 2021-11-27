# Changelog


### Latest

* BUGFIX : Fixed setup.py pointing to README.rst instead of README.md.


### 0.3.5


No relevant code changes.

### 0.3.4

* FEATURE : Added stdout_to_filename and from_filename.


### 0.3.3


No relevant code changes.

### 0.3.2

* FEATURE : .output() returns piped output.


### 0.3.1

* FEATURE : PipedCommand object.
* FEATURE : Run piped commands through PipedCommand object.


### 0.3.0

* MINOR : FEATURE : Added interactive link to create an icommandlib object.
* MINOR : FEATURE : Add the ability to use the python or virtualenv's bin as a CommandPath object.
* MINOR : FEATURE : Pipe to stdin from string.


### 0.2.7

* FEATURE : Added a command to run python using the current shell/interpreter.


### 0.2.6

* BUG : Adding contents of the existing PATH variable should be added to the new PATH, not the other way around.


### 0.2.5

* FEATURE : Added output getter from commands.


### 0.2.4

* FEATURE : Added pexpect ability to commandlib.


### 0.2.3

* BUG : Fixed pipe error.


### 0.2.2

* FEATURE : Importable CommandError.


### 0.2.1

* FEATURE : Put back deprecated Commands class.


### 0.2

* FEATURE : You can now pipe in from stdin.
* FEATURE : Pipe to stdout/stderr and refactor.


### 0.1.8

* BUG : without_env failed when the environment variable did not exist.


### 0.1.7

* FEATURE : Made commandlib more production-ready


### 0.1.6

* BUG : Fixed the 'Commands' object and added docs.


### 0.1.5

* BUG : Cast directory to string.


### 0.1.4

* BUG : Fixed 'shell' and ignore errors bugs.


### 0.1.3

* BUG : Fixed subprocess PIPE import error.


### 0.1.2

* BUG : Fixed _shell problem


### 0.1.1

* BUG : _silent_* properties must be set to false on initialization.

