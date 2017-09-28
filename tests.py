#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os
import unittest
import tempfile
import shutil
from vagrep.fileutils.file_tools import filter_filenames_by_re,\
                                        filter_relpath_by_re,\
                                        get_files_from_dir,\
                                        get_files_from_dir_rec


def touch(path):
    with open(path, 'a'):
        os.utime(path, None)


class TestFileUtilMethods(unittest.TestCase):
    def test_get_files_funcs(self):
        work_folder = tempfile.mkdtemp()
        filenames = ['aaa.txt', 'bbb.txt']
        for f in filenames:
            touch(os.path.join(work_folder, f))
        inner_folder = os.path.join(work_folder, 'inner')
        os.mkdir(inner_folder)
        inner_filenames = ['zzz', 'ppp', 'qqq']
        for f in inner_filenames:
            touch(os.path.join(inner_folder, f))

        should_be = [os.path.join(work_folder, f) for f in filenames]

        print set(should_be)
        self.assertSetEqual(set(should_be),
                            set(get_files_from_dir(work_folder)))

        for f in inner_filenames:
            should_be.append(os.path.join(inner_folder, f))

        print set(should_be)
        self.assertSetEqual(set(should_be),
                            set(get_files_from_dir_rec(work_folder)))

        inner_empty_folder = os.path.join(work_folder, 'inner_empty')
        os.mkdir(inner_empty_folder)

        should_be = []

        print(set(should_be))
        self.assertSetEqual(set(should_be),
                            set(get_files_from_dir(inner_empty_folder)))
        self.assertSetEqual(set(should_be),
                            set(get_files_from_dir_rec(inner_empty_folder)))

        shutil.rmtree(work_folder)

if __name__ == '__main__':
    unittest.main()
