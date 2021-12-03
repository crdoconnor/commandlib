---
title: Piping data in from string or file (.piped)
---





bin_directory/command1:
```bash
#!/bin/bash
read X
echo hello $X > output

```


```python
from commandlib import CommandPath
command_path = CommandPath("./bin_directory")

```




from string:




```python
with open("person", "r") as handle:
    command_path.command1().piped.from_string("harry").run()

```






File 'output' will contain:
```
hello harry
```



from file handle:




```python
with open("person", "r") as handle:
    command_path.command1().piped.from_handle(handle).run()

```






File 'output' will contain:
```
hello harry
```



from filename:




```python
command_path.command1().piped.from_filename("person").run()

```






File 'output' will contain:
```
hello harry
```







!!! note "Executable specification"

    Documentation automatically generated from 
    <a href="https://github.com/crdoconnor/commandlib/blob/master/hitch/story/pipe.story">pipe.story
    storytests.
