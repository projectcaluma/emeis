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
    include_package_data=True,
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
        "django-cors-headers>=3.7.0,<4",
        "django-environ<0.9",
        "django-filter<22",
        "django-generic-api-permissions<1",
        "django-localized-fields>=6.4,<7",
        "django_mptt>=0.11,<2",
        "django-postgres-extra<3",
        "djangorestframework>=3.12.4,<4",
        "djangorestframework-jsonapi>=4.3.0,<=5.0.0",
        "mozilla-django-oidc<3",
        "pyexcel>0.6,<1",
        "pyexcel-xlsx>=0.6.0,<1",
        "psycopg2>=2.9,<3",
        "requests<3",
        "uwsgi<3",
        "openpyxl<4",
    ],
)
