#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


import setuptools


setuptools.setup(
    name='vagrep',
    version='1.0',
    author='Alex Vistyazh',
    author_email='alexvistyazh@gmail.com',
    description='CLI tool for searching in files',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'vagrep = vagrep.main:main',
        ]
    }
)
