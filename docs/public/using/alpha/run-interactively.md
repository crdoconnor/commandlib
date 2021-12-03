---
title: Run commmands interactively using icommandlib or pexpect
---


However, if the command you want to run requires that:

* It prompts the user for a response (yes or no / password / etc.)
* It 'draws' on a terminal window - like 'top'.
* You want to interact with the process and do other stuff while it runs
(e.g. wait for a database service to warm up and then continue).

Then you need an interactive library.

Commandlib can call and create an interactive process object for two
other libraries this way - [ICommandLib](https://github.com/crdoconnor/icommandlib)
and [pexpect](https://pexpect.readthedocs.io/en/stable/).

The two examples below are not actually interactive but they demonstrate
how pexpect and icommandlib can be used.



outputtext:
```bash
#!/bin/bash
echo hello $1

```


```python
from commandlib import Command

```




icommandlib:




```python
process = Command("./outputtext", "mark").interactive().run()
process.wait_until_output_contains("mark")
process.wait_for_successful_exit()

```






pexpect:




```python
from pexpect import EOF
process = Command("./outputtext", "mark").pexpect()
process.expect("mark")
process.expect(EOF)
process.close()

```










!!! note "Executable specification"

    Documentation automatically generated from 
    <a href="https://github.com/crdoconnor/commandlib/blob/master/hitch/story/icommand-or-pexpect.story">icommand-or-pexpect.story
    storytests.
