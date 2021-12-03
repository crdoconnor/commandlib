---
title: Run command and don't raise exception on nonzero exit code (ignore_errors())
---





outputtext:
```bash
#!/bin/bash
echo hello > output
exit 1

```


```python
from commandlib import Command
```






```python
Command("./outputtext").ignore_errors().run()
```






File 'output' will contain:
```
hello
```






!!! note "Executable specification"

    Documentation automatically generated from 
    <a href="https://github.com/crdoconnor/commandlib/blob/master/hitch/story/ignore-errors.story">ignore-errors.story
    storytests.
