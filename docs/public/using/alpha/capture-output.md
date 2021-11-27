---
title: Capture output (.output())
type: using
---


You can run a command and capture the stdout and stderr to a string
using .output().

This is unsuitable for:

* Capturing output from programs that draw all over the screen (like top).
* Capturing output from programs that output special terminal characters (e.g. color characters).
* Interacting with programs that use user input.

For all of the above use cases and more, command.interact() is more suitable.



outputtext:
```bash
#!/bin/bash
echo hello from stdout
>&2 echo "hello from stderr"

```
raiseerror:
```bash
#!/bin/bash
echo bad output from stdout
>&2 echo "bad output from stderr"
exit 1

```


```python
from commandlib import Command
```




Success:




```python
assert Command("./outputtext").output().strip() \
  == "hello from stdout\nhello from stderr"

```






Error:




```python
Command("./raiseerror").output().strip()
```


```python
commandlib.exceptions.CommandExitError:
"./raiseerror" failed (err code 1), output:

bad output from stdout
bad output from stderr
```










{{< note title="Executable specification" >}}
Page automatically generated from <a href="https://github.com/crdoconnor/commandlib/blob/master/hitch/capture-output.story">capture-output.story</a>.
{{< /note >}}
