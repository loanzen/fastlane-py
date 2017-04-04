#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup


requirements = [
    "requests"
]

setup(
    name='fastlane',
    version='0.1.1',
    description="",
    long_description='',
    author="Kshitij Mittal",
    author_email='kshitij@loanzen.in',
    url='https://github.com/loanzen/fastlane-py',
    packages=[
        'fastlane',
    ],
    package_dir={'fastlane':
                 'fastlane'},
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
)
