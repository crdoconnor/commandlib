CommandLib
==========

CommandLib is a more pythonic wrapper around subprocess libs that lets you
pass around command objects and daisy-chain:

* Arguments
* Environment variables
* Runtime directory
* Other runtime properties (use shell, conceal stdout/stderr, ignore error codes, etc.)

It is somewhat inspired by amoffat's sh (albeit with less magic), Kenneth Reitz's
requests, jaraco's path.py and SQLAlchemy.


Examples::

    >>> from commandlib import Command, run
    >>> ls = Command("ls", shell=True)
    >>> run(ls("-t").in_dir("/"))
    sys  tmp  run  dev  proc  etc  boot  sbin  root  vmlinuz  initrd.img  bin  lib  opt  vmlinuz.old  initrd.img.old  media  home  cdrom  lost+found  var  srv  usr  mnt


Install
-------

   pip install commandlib


Hacking
-------

If you want to hack, you can TDD with::

  sudo pip install hitch
  cd tests
  hitch init
  hitch test . --settings tdd.settings
