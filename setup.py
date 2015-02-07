#!/usr/bin/env python

from distutils.core import setup

setup(
    name="gitpatrol",
    version="0.01",
    description="Flexible Git Pre-Commit Hooks",
    author="Arthur Burkart",
    author_email="artburkart@gmail.com",
    url="https://github.com/artburkart/gitpatrol",
    packages=["gitpatrol"],
    setup_requires=["nose>=1.3.4", "parameterizedtestcase==0.1.0"]
)
