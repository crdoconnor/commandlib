{% if readme -%}
# CommandLib
{%- else -%}
---
title: CommandLib
---

{% raw %}{{< github-stars user="crdoconnor" project="commandlib" >}}{% endraw %}
{% endif %}

Commandlib is an ergonomic library that lets you build pseudo-immutable UNIX command
objects using method chaining:

{% for story in quickstart %}
{% for name, script in story.given.get('scripts', {}).items() %}
Pretend '{{ name }}':
```bash
{{ script }}
```
{%- endfor %}

```python
{{ story.given['setup'] }}
```

{% with step = story.steps[0] %}{% include "step.jinja2" %}{% endwith %}
{% endfor %}

You can also:

{% for dirfile in subdir("using/alpha/").is_not_dir() - subdir("using/alpha/").named("index.md") -%}
- [{{ title(dirfile) }}](using/alpha/{{ dirfile.namebase }})
{% endfor %}

The tool was originally created to clean a lot of dirty build code that
called subprocess. Like every other library in the world it was written for
humans ;-)

Install
-------

```sh
$ pip install commandlib
```
