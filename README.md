# Git Patrol
The goal is to create a plug and play git pre-commit hook that completes a bunch
of basic checks, but also lints each file with its language's respective linter.


Deeply inspired by Bob Gilmore's [githooks](https://travis-ci.org/bobgilmore/githooks)

# Installation:
1. `pip install gitpatrol`
1. `cd {location/of/your/repo}`
1. `gitpatrol init`
1. Add a `gitpatrol.toml` file to root folder (samples
are [here](https://github.com/artburkart/gitpatrol/tree/master/example_configs))
1. Make some changes to some files in your repo that do not respect
the checkers in your `gitpatrol.toml` file
1. Stage your changes for commit
1. `git commit`
  1. You should get output that looks like this:
  ![Git Patrol output](./gitpatrol_output.png)
  1. The value in quotations marks at the beginning of each line is the offending character sequence, which your checker found
  1. The values in parentheses reference the checkers defined in the `gitpatrol.toml` file, which have found a problem with your commit
1. Your commit will be blocked until the checkers are happy (or you disable them)



# Development
I would love it if you used the Issue Tracker to notify me of PRs
you'd like to contribute to this project. There are a couple things I'd like to
implement next. You can see them in the [TODO.md](./TODO.md)

# To run tests
1. Clone the project from its [GitHub repo](https://github.com/artburkart/gitpatrol)
1. `pip install -r dev-requirements`
1. `nosetests`
  1. `nosetests --with-coverage --cover-html --cover-branches` (runs with coverage)
