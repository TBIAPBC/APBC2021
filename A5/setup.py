import setuptools
from setuptools import setup, find_packages





with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Lorenzo360_A5", # Replace with your own username
    version="1.0.0",
    author="Lorenzo360",
    author_email="author@example.com",
    description="Contains a collection of programs written for the course Algorithmen und Programmentwicklung für die Biologische Chemie",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TBIAPBC/APBC2021",
    project_urls={
        "Bug Tracker": "https://github.com/TBIAPBC/APBC2021/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    entry_points={"console_scripts": ["Lorenzo360_A5 = Lorenzo360_A5.__main__:main",],},
    include_package_data = True,
    python_requires=">=3.6",
    install_requires=[ "numpy","argparse"]
    
)
