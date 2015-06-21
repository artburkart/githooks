==========
Git Patrol
==========

The goal is to create a plug and play git pre-commit hook that completes
a bunch of basic checks, but also lints each file with its language's
respective linter.

Deeply inspired by Bob Gilmore's
`githooks <https://travis-ci.org/bobgilmore/githooks>`__

To Install:
``pip install gitpatrol``

Git Patrol API
==============
## NOTE: None of the CLI has been implemented yet. It's in the pipeline! For now, all you can do is run ``gitpatrol`` or ``gitpatrol install`` to install Git Patrol into a repo.

gitpatrol.hooks.{hookname}.enabled
gitpatrol.hooks.{hookname}.tempenabled
gitpatrol.hooks.{hookname}.tempdisabled

I want to enable a hook forever I want to disable a hook forever
``gitpatrol.hooks.{hookname}.enabled {true/false}``

I want to enable a hook for the duration of one commit
``gitpatrol.hooks.{hookname}.tempenabled {true/false}``

I want to disable a hook for the duration of one commit
``gitpatrol.hooks.{hookname}.tempdisabled {true/false}``

I want to *permanently* ignore a file or directory for a hook
``gitpatrol.hooks.{hookname}.ignore {filepath/directory/regular expression}``

I want to ignore multiple files /andor directories permanently for a
hook ``gitpatrol.hooks.{hookname}.ignore {file1,directory2}``

Same rules of ignore apply for tempignore, except tempignore resets
after next commit \`gitpatrol.hooks.{hookname}.tempignore file1

Just use 'all' for ignoring and temp ignoring files and directories
``gitpatrol.hooks.all.{ignore/tempignore} {file1/directory1/file1,directory1/regex1,regex2}``

To run tests
============

``nosetests`` from the root directory

To run tests with coverage
==========================

``nosetests --with-coverage --cover-html --cover-branches``
