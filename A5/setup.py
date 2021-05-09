#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  7 14:44:42 2021

@author: milan
"""

from setuptools import setup, find_packages

VERSION = "1.0.10"
DESCRIPTION = "MilanG's Python package for APBC A0-A4"
with open("README.md", "r") as fh_readme:
    LONG_DESCRIPTION = fh_readme.read()


setup(
        name="MilanG-git_A5", 
        version=VERSION,
        author="Milan Geyer",
        author_email="milan.geyer@gmx.at",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type = "text/markdown",
        packages=find_packages(),
        install_requires=["numpy"], 
        entry_points={"console_scripts": ["MilanG-git_A5 = MilanG_A5.__main__:main",],},
        keywords=["python", "first package", "APBC2021"],
        classifiers= [
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
        ]
)