#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import re


class TerminalColors(object):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def disable_colors(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''


class Processor(object):
    def match(self, line):
        raise NotImplementedError(
            "Define method match in %s." % (self.__class__.__name__))

    def process(self, fname, lcontext, line, rcontext):
        raise NotImplementedError(
            "Define method process in %s." % (self.__class__.__name__))


class Consumer(object):
    def consume(self, lcontext, line, rcontext):
        raise NotImplementedError(
            "Define method consume in %s." % (self.__class__.__name__))

    def fihish(self):
        raise NotImplementedError(
            "Define method finish in %s." % (self.__class__.__name__))


def formatted_occurences(line, prog):
    occurences = [[x.start(), x.end()] for x in prog.finditer(line)]
    if len(occurences) == 0:
        return line
    else:
        concatlist = []
        concatlist.append(line[0:occurences[0][0]])
        for i in xrange(len(occurences)):
            borders = occurences[i]
            cur = TerminalColors.UNDERLINE + TerminalColors.BOLD +\
                TerminalColors.OKGREEN +\
                line[borders[0]:borders[1]] + TerminalColors.ENDC
            concatlist.append(cur)
            borders = [occurences[i][1],
                       -1 if i + 1 == len(occurences) else occurences[i + 1][0]]
            cur = line[borders[0]:borders[1]]
            concatlist.append(cur)
        return ''.join(concatlist)


class ConsumerPattern(Consumer):
    """
    Something like logger for output result of grep for one file
    """
    def __init__(self, fname, out):
        self.fname = fname
        self.out = out

    def consume(self, lcontext, line, index, rcontext, prog):
        lcontext = filter(lambda x: len(x) > 0, lcontext)
        rcontext = filter(lambda x: len(x) > 0, rcontext)
        if len(lcontext) == 0:
            lres = ''
        else:
            lres = 'Left context:\n' + '\n'.join(lcontext) + '\n'
        if len(rcontext) == 0:
            rres = ''
        else:
            rres = 'Right context:\n' + '\n'.join(rcontext) + '\n'
        res = '{lcontext}'\
              '{path}:{index}: {res}\n'\
              '{rcontext}'\
              .format(lcontext=lres,
                      path=TerminalColors.HEADER + self.fname +
                      TerminalColors.ENDC,
                      index=TerminalColors.OKBLUE + str(index) +
                      TerminalColors.ENDC,
                      res=formatted_occurences(line, prog),
                      rcontext=rres)
        self.out.write(res)

    def finish(self):
        pass


class ConsumerCounter(Consumer):
    """
    Consumer which outputs number of found lines in file
    """
    def __init__(self, fname, out):
        self.fname = fname
        self.out = out
        self.counter = 0

    def consume(self, *args):
        self.counter += 1

    def finish(self):
        res = '{path}: {cnt} lines are found\n'\
              .format(path=TerminalColors.HEADER + self.fname +
                      TerminalColors.ENDC,
                      cnt=self.counter)
        self.out.write(res)


class ProcessorByPattern(Processor):
    def __init__(self, r, inverse):
        self.prog = re.compile(r)
        self.inverse = inverse

    def match(self, line):
        if not self.inverse:
            return self.prog.search(line)
        else:
            return not self.prog.search(line)

    def process(self, consumer, lcontext, line, index, rcontext):
        consumer.consume(lcontext, line, index, rcontext, self.prog)
