"""Setuptools package definition."""

import os

from setuptools import find_packages, setup

version = {}
with open("emeis/emeis_metadata.py") as fp:
    exec(fp.read(), version)


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


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
    install_requires=[
        "django~=3.2",
        "django-cors-headers >=3.7.0, <=3.13.1",
        "django-environ==0.8.1",
        "django-filter==21.1",
        "django-generic-api-permissions==0.2.0",
        "django-localized-fields>=6.4,<=6.6",
        "django_mptt>=0.11,<=0.13.4",
        "django-postgres-extra==2.0.3",
        "djangorestframework>=3.12.4,<=3.13.1",
        "djangorestframework-jsonapi>=4.3.0,<=5.0.0",
        "mozilla-django-oidc==1.2.4",
        "pyexcel==0.6.7",
        "pyexcel-xlsx==0.6.0",
        "requests==2.26.0",
        "uwsgi==2.0.19.1",
        "openpyxl==3.0.9",
    ],
)
