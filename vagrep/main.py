#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import argparse
import multiprocessing
import vagrep.fileutils.file_tools as ftools
import vagrep.searchers.funcs as funcs
import vagrep.processors.processor as processor
import os
import sys
from vagrep.processors.processor import TerminalColors


def main():
    parser = argparse.ArgumentParser()

    target = parser.add_mutually_exclusive_group()
    target.add_argument('--files', nargs='*', help='files to search')
    target.add_argument('--folders', nargs='*',
                        help='in which folders use files (only files in folder')
    target.add_argument('--foldersrec', nargs='*',
                        help='folders (recursively) in which use files')

    group_path_regex = parser.add_mutually_exclusive_group()
    group_path_regex.add_argument('--relregex', help='regex for relative path')
    group_path_regex.add_argument('--absregex', help='regex for absolute path')

    parser.add_argument('-L', type=int,
                        help='how many lines take to context before found line')
    parser.add_argument('-R', type=int,
                        help='how many lines take to context after found line')
    parser.add_argument('-A', type=int,
                        help='how many lines take to context around found line')
    parser.add_argument('-i', '--inverse', action='store_true', default=False)

    parser.add_argument('-c', '--count', action='store_true', default=False)
    parser.add_argument('--disablecolor', action='store_true', default=False)

    group_find = parser.add_mutually_exclusive_group(required=True)
    group_find.add_argument('--pattern', help='what to find (regex)')
    group_find.add_argument('--text', help='what to find (text)')

    args = parser.parse_args()

    if args.A is not None and (args.L is not None or args.R is not None):
        parser.error('only one can be set [-A | [-L L -R R]]')

    if (args.A is not None or args.L is not None or args.R is not None)\
            and args.count:
        parser.error('you dont need to count lines '
                     'and print context simultaneously')

    bef, aft = 0, 0

    if args.A is not None:
        if args.A < 0:
            parser.error('-A argument accepts only non-negative integer')
        bef = args.A
        aft = args.A
    else:
        if args.L is not None:
            if args.L < 0:
                parser.error('-L argument accepts only non-negative integer')
            bef = args.L
        if args.R is not None:
            if args.R < 0:
                parser.error('-R argument accepts only non-negative integer')
            aft = args.R

    if args.disablecolor:
        TerminalColors.disable_colors()

    if args.relregex is not None:
        def files_receiver(dpath, files):
            return ftools.filter_relpath_by_re(dpath, files, args.relregex)
    elif args.absregex is not None:
        def files_receiver(_, files):
            return ftools.filter_filenames_by_re(files, args.absregex)
    else:
        def files_receiver(_, files):
            return ftools.filter_filenames_by_re(files, '.*')

    if args.pattern is not None:
        pr = processor.ProcessorByPattern(args.pattern, args.inverse)
    elif args.text is not None:
        args.pattern = ''.join(map(lambda x: '[' + x + ']', args.text))
        pr = processor.ProcessorByPattern(args.pattern, args.inverse)

    if args.count:
        def get_consumer(fname):
            return processor.ConsumerCounter(fname, sys.stdout)
    else:
        def get_consumer(fname):
            return processor.ConsumerPattern(fname, sys.stdout)

    if args.files is None:
        args.files = []
    if args.folders is None:
        args.folders = []
    if args.foldersrec is None:
        args.foldersrec = []

    def process_file(f):
        with open(f) as text:
            p = multiprocessing.Process(target=funcs.process_text,
                                        args=(get_consumer(f),
                                              text, pr, bef, aft))
            p.start()

    for original_f in args.files:
        f = os.path.abspath(original_f)
        if not os.path.isfile(f):
            parser.error('the item you pass to files is not exist: %s'
                         % original_f)
        process_file(f)

    for original_d in args.folders:
        d = os.path.abspath(original_d)
        if not os.path.isdir(d):
            parser.error('%s is not existing directory' % original_d)
        files = files_receiver(d, ftools.get_files_from_dir(d))
        for f in files:
            process_file(f)

    for original_d in args.foldersrec:
        d = os.path.abspath(original_d)
        if not os.path.isdir(d):
            parser.error('%s is not existing directory' % original_d)
        files = files_receiver(d, ftools.get_files_from_dir_rec(d))
        for f in files:
            process_file(f)


if __name__ == '__main__':
    main()
