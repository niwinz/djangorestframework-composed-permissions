#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import sys


INSTALL_REQUIRES = [
    "django >=1.4",
]

setup(
    name = "djangorestframework-composed-permissions",
    version = "0.1",
    description = "Composed permissions for django-rest-framework",
    long_description = "",
    keywords = "django, rest, restframework, permissions",
    author = "Andrey Antukh",
    author_email = "niwi@niwi.be",
    url = "https://github.com/niwibe/djangorestframework-composed-permissions",
    license = "BSD",
    packages = [
        'restfw_composed_permissions',
        'restfw_composed_permissions.generic',
    ],

    install_requires = INSTALL_REQUIRES,
    classifiers = [
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Topic :: Internet :: WWW/HTTP",
    ]
)
