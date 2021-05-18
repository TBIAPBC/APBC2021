#!/usr/bin/env python3
from __future__ import absolute_import
from setuptools import setup, find_packages


with open("README.md", "r") as fh_readme:
    LONG_DESCRIPTION = fh_readme.read()

setup(
    name="eerah-A5",
    version = "0.0.1",
    description = "Contains programs for the course Algorithmen und Programmentwicklung für die Biologische Chemie",
    author="Philipp Fischer",
    author_email="fischer-philipp@gmx.net",
    long_description=LONG_DESCRIPTION,
    long_description_content_type = "text/markdown",
    install_requires=["numpy", "pandas"],
    packages=find_packages(),
    entry_points={"console_scripts": ["eerah-A5=eerah_A5.__main__:main", ], },
    include_package_data=True,
    keywords=["APBC2021", "python3"],
    python_requires=">=3.6",
    classifiers= [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)

