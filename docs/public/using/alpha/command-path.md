---
title: Easily invoke commands from one directory (CommandPath)
type: using
---


A CommandPath is an object that you can create to represent
a directory with executables in it. You can then use that object
to get command objects which you can then run.

This feature was created to be able to create a "postgres" or "node"
or "virtualenv" CommandPath object referencing their bin directory.
Commands in those bin directories (e.g. postgres / psql) could be run
and be able to directly call *other* commands in that directory without
referencing the absolute path.

Command objects that are created from CommandPath objects 
will automatically be run with that directory added to the beginning
of their PATH. This means that they can run each other directly
without specifying the directory.



bin_directory/ls:
```bash
#!/bin/bash
echo hello $1 > output

```
bin_directory/command1:
```bash
#!/bin/bash
ls $1

```
bin_directory/command2:
```bash
#!/bin/bash
echo hello $1 > output

```
bin_directory/command_calling_command_in_path:
```bash
#!/bin/bash
command1 tom

```
bin_directory/command.with.dots:
```bash
#!/bin/bash
echo hello dots > output

```


```python
from commandlib import CommandPath

command_path = CommandPath("./bin_directory")

```




Run command from CommandPath:




```python
command_path.command1("harry").run()
```






File 'output' will contain:
```
hello harry
```



Command can call other command in CommandPath without specifying its path:




```python
command_path.command_calling_command_in_path("tom").run()
```






File 'output' will contain:
```
hello tom
```



Commands with dots in command path are translated into underscores:




```python
command_path.command_with_dots("tom").run()
```






File 'output' will contain:
```
hello dots
```



Referencing a non-existent command raises an exception:




```python
command_path.non_existent_command
```


```python
commandlib.exceptions.CommandError:
'non_existent_command' not found in '/path/to/bin_directory'
```










{{< note title="Executable specification" >}}
Page automatically generated from <a href="https://github.com/crdoconnor/commandlib/blob/master/hitch/command-path.story">command-path.story</a>.
{{< /note >}}
