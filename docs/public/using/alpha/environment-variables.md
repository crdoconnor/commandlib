---
title: Change your command's environment variables (with_env)
type: using
---


Environment variables can be set and passed down
to commands or, alternative, environment variables can
be explicitly dropped.

All parent environment variables will be passed on by
default.





```python
from commandlib import Command

```




With extra environment variable:




```python
Command("./outputtext").with_env(ENVVAR="tom").run()
```

Will output:
```
hello tom
```






Dropping an environment variable:




```python
Command("./outputpath").without_env("HOME").run()
```

Will output:
```
hello
```






Dropping nonexistent variable does nothing:




```python
Command("outputtext").without_env("NONEXISTENTVAR").with_path(".").run()
```

Will output:
```
hello
```










{{< note title="Executable specification" >}}
Page automatically generated from <a href="https://github.com/crdoconnor/commandlib/blob/master/hitch/environment-variables.story">environment-variables.story</a>.
{{< /note >}}
