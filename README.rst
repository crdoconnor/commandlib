CommandLib
==========

CommandLib is a pythonic wrapper around subprocess that lets you pass around command objects
and daisy-chain:

* Arguments
* Paths
* Other environment variables
* Runtime directory
* Other runtime properties (run in shell, conceal stdout/stderr, ignore error codes, etc.)

It is somewhat inspired by amoffat's sh, Kenneth Reitz's requests, jaraco's path.py
and SQLAlchemy.


Example::

    >>> from commandlib import Command, run
    >>> ls = Command("ls")
    >>> run(ls("-t").in_dir("/").with_shell())
    sys  tmp  run  dev  proc  etc  boot  sbin  root  vmlinuz  initrd.img  bin  lib  opt  vmlinuz.old  initrd.img.old  media  home  cdrom  lost+found  var  srv  usr  mnt


Install
-------

    pip install commandlib


API
---

    >>> from commandlib import Command, run
    >>> py = Command("/usr/bin/python")
    >>> py = py.with_env(PYTHONPATH="/home/user/pythondirectory")    # Run with *additional* variable PYTHONPATH (added to global environment when command is run)
    >>> py = py.with_path("/home/user/bin")                          # Run with additional path (added to PATH environment variable when command is run)
    >>> py = py.in_dir("/home/user/mydir")                           # Run in specified directory.
    >>> py = py.with_shell()                                         # Run with shell

Why
---

Commandlib is a library to make it easier to pass around command objects between different
modules and classes and incrementally modify the command's behavior in a readable way
- adding environment variables, paths, etc.

* call, check_call and Popen do not have the friendliest of APIs and code that uses them a lot can get ugly.
* sh has rather too much magic (e.g. overriding import).
* envoy and sarge are more focused on chaining commands rather than arguments.

Advanced API
------------

Add trailing arguments:

    >>> from commandlib import Command, run
    >>> manage = Command("/usr/bin/python").with_trailing_arguments("--settings", "local_settings.py").in_dir("projectdir")
    >>> run(manage("runserver"))    # Runs "/usr/bin/python manage.py runserver --settings local_settings.py"

Dynamically generate bin directories:

    >>> from commandlib import BinDirectory, Command, run
    >>> postgres94 = BinDirectory("/usr/lib/postgresql/9.4/bin/")
    >>> run(postgres94.postgres)


Hacking
-------

If you want to hack, you can TDD with::

  sudo pip install hitch
  cd tests
  hitch init
  hitch test . --settings tdd.settings
