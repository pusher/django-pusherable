#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import pusherable

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = pusherable.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

readme = open('README.md').read()

setup(
    name='django-pusherable',
    version=version,
    description="""Real time object access notifications via Pusher""",
    long_description=readme,
    author='Aaron Bassett, Pusher',
    author_email='aaron@rawtech.io, support@pusher.com',
    url='https://github.com/pusher/django-pusherable',
    packages=[
        'pusherable',
    ],
    include_package_data=True,
    install_requires=[
        "pusher",
    ],
    license="BSD",
    zip_safe=False,
    keywords='django-pusherable',
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
)
