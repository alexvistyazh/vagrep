#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os
import re

""" Helper functions for receiving the list of files """


def get_all_from_dir(dirpath):
    """
    Function for returning list of files and directories from given directory

    :param dirpath: path to directory
    :return: list of paths to files and directories
    """

    dirpath = os.path.abspath(dirpath)
    dpath, dirs, filenames = next(os.walk(dirpath))
    return [os.path.join(dpath, filename) for filename in (filenames+dirs)]


def get_files_from_dir(dirpath):
    """
    Function for returning list of files from given directory

    :param dirpath: path to directory
    :return: list of paths to files
    """

    dirpath = os.path.abspath(dirpath)
    dpath, _, filenames = next(os.walk(dirpath))
    return [os.path.join(dpath, filename) for filename in filenames]


def get_files_from_dir_rec(dirpath):
    """
    Function for returning generator of files from given directory
        and sub-directories and etc.

    :param dirpath: path to directory
    :return: generator for paths to files
    """

    dirpath = os.path.abspath(dirpath)
    for dpath, _, filenames in os.walk(dirpath):
        for filename in filenames:
            yield os.path.join(dpath, filename)


def filter_filenames_by_re(filepaths, r):
    """
    Function for returning generator of files which names match to
        given regular expression.

    :param filespaths: paths to files
    :param r: given regexp as string
    :return: generator for paths to files which names match to regexp
    """

    prog = re.compile(r)
    for filepath in filepaths:
        filename = os.path.basename(filepath)
        if prog.match(filename):
            yield filepath


def filter_relpath_by_re(dirpath, filepaths, r):
    """
    Function for returning generator of files which relative path
        match to given regular expression.

    :param dirpath: path to directory in which files are located
    :param filepaths: paths to files
    :return: generator for paths of files which relative paths match to regexp
    """

    prog = re.compile(r)
    dirpath = os.path.abspath(dirpath)
    for filepath in filepaths:
        relpath = os.path.relpath(filepath, dirpath)
        if prog.match(relpath):
            yield filepath
