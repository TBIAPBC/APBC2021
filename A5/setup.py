#!/usr/bin/env python3
from setuptools import find_packages, setup

VERSION = "1.0.0"
DESCRIPTION = "Python package containing the tasks of the course APBC2021 from Markus Beicht"
with open("README.md", "r") as f:
    LONG_DESCRIPTION = f.read()


setup(
        name="MarkusBeicht-A5", 
        version=VERSION,
        author="Markus Beicht",
        author_email="markus.beicht@gmx.at",
        url="https://github.com/TBIAPBC/APBC2021",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type = "text/markdown",
        packages=find_packages(),
        install_requires=["numpy"], 
        entry_points={"console_scripts": ["MarkusBeicht_A5 = MarkusBeicht_A5.__main__:main",],},
        keywords=["APBC2021", "python3"],
        classifiers= [
        "Programming Language :: Python :: 3", 
        "Operating System :: OS Independent", 
        "License :: OSI Approved :: MIT License"
        ]
)
