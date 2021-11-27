---
title: Run command and don't raise exception on nonzero exit code (ignore_errors())
type: using
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






{{< note title="Executable specification" >}}
Page automatically generated from <a href="https://github.com/crdoconnor/commandlib/blob/master/hitch/ignore-errors.story">ignore-errors.story</a>.
{{< /note >}}
