---
title: Add directory to PATH (with_path)
type: using
---


If you want to run a command with an additional folder on
the path you can specify it with with_path.

Note that if you use [CommandPath](../command-path) object,
the directory you use it on is already added.



bin_directory/ls:
```bash
#!/bin/bash
echo hello $1 > output

```
runls:
```bash
#!/bin/bash
ls $1

```


```python
from commandlib import Command

runls = Command("./runls")

```




Add bin_directory to PATH for runls:




```python
runls("harry").with_path("bin_directory").run()
```






File 'output' will contain:
```
hello harry
```







{{< note title="Executable specification" >}}
Page automatically generated from <a href="https://github.com/crdoconnor/commandlib/blob/master/hitch/with-path.story">with-path.story</a>.
{{< /note >}}
