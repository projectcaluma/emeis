"""Setuptools package definition."""

import os

from setuptools import find_packages, setup

version = {}
with open("emeis/emeis_metadata.py") as fp:
    exec(fp.read(), version)


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


def deps_from_file(filename):
    lines = [line.strip().split("#")[0] for line in open(filename).readlines()]
    # filter out comment lines
    return [line for line in lines if line and not line == "-r requirements-base.txt"]


dependencies = deps_from_file("requirements-base.txt") + deps_from_file(
    "requirements-prod.txt"
)


setup(
    name=version["__title__"],
    version=version["__version__"],
    description=version["__description__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="projectcaluma",
    url="https://github.com/projectcaluma/emeis",
    license="License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    install_requires=dependencies,
)
