---
title: Piping data out to string or file (.piped)
type: using
---





bin_directory/command1:
```bash
#!/bin/bash
echo hello $1

```
bin_directory/command2:
```bash
#!/bin/bash
echo hello $1 1>&2

```


```python
from commandlib import CommandPath
command_path = CommandPath("./bin_directory")

```




stdout to file handle:




```python
with open("regular", "w") as handle:
    command_path.command1("harry").piped.stdout_to_handle(handle).run()

```






File 'regular' will contain:
```
hello harry
```



stdout to filename:




```python
command_path.command1("harry").piped.stdout_to_filename("regular").run()

```






File 'regular' will contain:
```
hello harry
```



stderr to file handle:




```python
with open("error", "w") as handle:
    command_path.command2("tom").piped.stderr_to_handle(handle).run()

```






File 'error' will contain:
```
hello tom
```







{{< note title="Executable specification" >}}
Page automatically generated from <a href="https://github.com/crdoconnor/commandlib/blob/master/hitch/pipe.story">pipe.story</a>.
{{< /note >}}
