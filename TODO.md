# 1. Implement plugins
The idea behind this is that I'd like to be able to write a gitpatrol.toml
configuration that looks like the following:
```
[plugins.jshint]
command = 'jshint'
enabled = true
```
It would fire off whatever command is specified by the `command` key.
One problem that may arise from this is that each plugin may
exit differently. Exit codes or outputs may need to be captured, which could
get ugly.

# 2. Implement Git Patrol API in CLI
* I want to enable/disable a hook forever

  `gitpatrol.hooks.{hookname}.enabled {true/false}`

---

* I want to enable a hook for the duration of one commit

  `gitpatrol.hooks.{hookname}.tempenabled {true/false}`

---

* I want to disable a hook for the duration of one commit

  `gitpatrol.hooks.{hookname}.tempdisabled {true/false}`

---

* I want to *permanently* ignore a file or directory for a hook

  `gitpatrol.hooks.{hookname}.ignore {filepath/directory/regular expression}`

---

* I want to ignore multiple files /andor directories permanently for a hook

  `gitpatrol.hooks.{hookname}.ignore {file1,directory2}`

---

* Same rules of ignore apply for tempignore, except tempignore resets after next
commit

  `gitpatrol.hooks.{hookname}.tempignore file1

---

* Just use 'all' for ignoring and temp ignoring files and directories

  `gitpatrol.hooks.all.{ignore/tempignore} {file1/directory1/file1,directory1/regex1,regex2}`
