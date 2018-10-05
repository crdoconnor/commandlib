{% if readme -%}
# CommandLib
{%- else -%}
---
title: CommandLib
---

{% raw %}{{< github-stars user="crdoconnor" project="commandlib" >}}{% endraw %}
{% endif %}

Commandlib is a dependencyless library for writing clean, readable code that runs a lot of
UNIX commands (e.g. in build scripts). It avoids the tangle of messy code that you would
get using the subprocess library directly (Popen, call, check_output(), .communicate(), etc.).

Using method chaining, you can build up Command objects that run in a specific
directory, with specified [environment variables](using/alpha/environment-variables)
and [PATHs](using/alpha/add-directory-to-path), etc.

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


Install
-------

```sh
$ pip install commandlib
```

Docs
----

{% for dirfile in subdir("using/alpha/").is_not_dir() - subdir("using/alpha/").named("index.md") -%}
- [{{ title(dirfile) }}](using/alpha/{{ dirfile.namebase }})
{% endfor %}
