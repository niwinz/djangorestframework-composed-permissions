#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as file:
    long_description = file.read()

INSTALL_REQUIRES = [
    "django >= 1.11",
    "djangorestframework",
]

setup(
    name="djangorestframework-composed-permissions",
    version="0.2.1",
    description="Composed permissions for django-rest-framework",
    long_description=long_description,
    keywords="django, rest, restframework, permissions",
    author="Andrey Antukh",
    author_email="niwi@niwi.be",
    url="https://github.com/niwibe/djangorestframework-composed-permissions",
    license="BSD",
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP",
    ]
)
