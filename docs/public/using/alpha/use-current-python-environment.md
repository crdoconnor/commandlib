---
title: Easily invoke commands from the current virtualenv (python_bin)
---


You can run python code in the same environment
by importing "python" command object or the
"python_bin" command path.

If you are running the code in a virtualenv, for
example, the python object will refer to the python
binary in the virtualenv bin directory.



outputtext.py:
```bash
with open("output", "w") as handle:
    handle.write("hello")

```


```python
from commandlib import python, python_bin

```




Run python:




```python
python("outputtext.py").run()
```






File 'output' will contain:
```
hello
```



Use python_bin:




```python
python_bin.python("outputtext.py").run()
```






File 'output' will contain:
```
hello
```







!!! note "Executable specification"

    Documentation automatically generated from 
    <a href="https://github.com/crdoconnor/commandlib/blob/master/hitch/story/run-python.story">run-python.story
    storytests.
