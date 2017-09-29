#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from collections import deque
import itertools


def generator_poll(iterable):
    """
    return first element from iterable and remove it,
        if iterable is empty then return None
    """
    try:
        res = next(iterable)
    except StopIteration:
        return None
    return res


def deque_slice(d, l, r):
    if r == -1:
        r = len(d)
    return list(itertools.islice(d, l, r))


def process_text(consumer, text, processor, bef=0, aft=0):
    """
    Function which process text line by line and find lines which match to
        matcher in processor.
        Also found lines return to processor with context.
    :param fname: name of file in which we do search
    :param text: lines of file fname
    :param processor: object which have matcher and we return found lines to it
    :param bef: how many lines before should be in context
    :param aft: how many lines after should be in context
    """

    text = (line[0:len(line)-1] for line in text)

    deqleft = 0
    deqright = -1
    deq = deque()
    index = -1
    while True:
        index += 1
        while deqright < index + aft:
            cur = generator_poll(text)
            if cur is None:
                break
            deq.append(cur)
            deqright += 1
        if index > deqright:
            break
        while deqleft < index - bef:
            deq.popleft()
            deqleft += 1
        if index < deqleft:
            break
        line = deq[index - deqleft]
        if processor.match(line):
            processor.process(consumer, deque_slice(deq, 0, index - deqleft),
                              line, index,
                              deque_slice(deq, index - deqleft + 1, -1))
    consumer.finish()
