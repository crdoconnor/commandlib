# CommandLib

Commandlib is a dependencyless library for calling external UNIX commands
(e.g. in build scripts) in a clean, readable way.

Using method chaining, you can build up Command objects that run in a specific
directory, with specified [environment variables](https://hitchdev.com/commandlib/using/alpha/environment-variables)
and [PATHs](https://hitchdev.com/commandlib/using/alpha/add-directory-to-path), etc.

For simplicity's sake, the library itself only runs commands in a blocking
way (all commands run to completion before continuing), although it contains
hooks to run non-blocking via either [icommandlib](https://github.com/crdoconnor/icommandlib)
or [pexpect](https://pexpect.readthedocs.io/en/stable/).



Pretend 'django/manage.py':
```bash
# Pretend django "manage.py" that just prints out arguments:
import sys ; sys.stdout.write(' '.join(sys.argv[1:]))

```

```python
from commandlib import Command

# Create base command
python = Command("python")

# Create command "python manage.py" that runs in the django directory
manage = python("manage.py").in_dir("django")

# Build even more specific command
dev_manage = manage.with_trailing_args("--settings", "local_settings.py")

```



```python
# Run combined command
dev_manage("runserver", "8080").run()

```

Will output:
```
runserver 8080 --settings local_settings.py
```






## Install

```sh
$ pip install commandlib
```

## Docs



## Why?

Commandlib avoids the tangle of messy code that you would
get using the subprocess library directly (Popen, call, check_output(), .communicate(), etc.)
and the [confusion that results](https://stackoverflow.com/questions/89228/calling-an-external-command-in-python).

It's a [heavily dogfooded](https://hitchdev.com/principles/extreme-dogfooding) library.

## Why not use Delegator instead (Kenneth Reitz's 'subprocesses for humans')?

Kenneth Reitz (author of requests "urllib2/3 for humans"), wrote a similarly inspired "subprocess for humans"
called [envoy](https://github.com/kennethreitz/envoy). That is now deprecated and there is now a replacement called [delegator](https://github.com/kennethreitz/delegator.py), which is a very thin
wrapper around subprocess.

Features delegator has which commandlib does not:

* Delegator can chain commands, much like bash does (delegator.chain('fortune | cowsay')). Commandlib doesn't do that because while dogfooding the library I never encountered a use case where I found this to be necessary. You can, however, easily get the output of one command using .output() as a string and feed it into another using piped.from_string(string).

* Delegator runs subprocesses in both a blocking and nonblocking way (using pexpect). commandlib only does blocking by itself but if you pip install pexpect or icommandlib it can run via either one of them.

Features which both have:

* Ability to set environment variables.
* Ability to run pexpect process from command object.

Features which only commandlib has:

* Ability to set PATH easily.
* Ability call code from within the current virtualenv easily.
* Ability to pipe in strings or files and easily pipe out to strings or file (or file handles).

## Why not use other tools?

* subprocess - if you just call one or two external commands, it's probably fine, but beyond that it will become a mess.

* os.system(*) - only capable of running simple bash commands.

* [sh](https://amoffat.github.io/sh/) - uses a lot of magic. Attempts to make python more like shell rather than making running commands more pythonic.

* [plumbum](https://plumbum.readthedocs.io/en/latest/]) - similar to amoffat's sh, tries to make a sort of "bash inside python". Also has a weird way of building commands from dict syntax (grep["-v", "\\.py"]).