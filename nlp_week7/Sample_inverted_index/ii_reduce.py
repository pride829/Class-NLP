#!/usr/bin/env python
# -*- coding: utf-8 -*-
from itertools import groupby
from operator import itemgetter


def inverted_index_reduce(items):
    for word, word_lines in groupby(items, key=itemgetter(0)):
        line_numbers = [line_no for _, line_no in word_lines]
        yield word, line_numbers


if __name__ == '__main__':
    import fileinput
    iterable = map(str.split, fileinput.input())
    for word, line_numbers in inverted_index_reduce(iterable):
        print(word, *line_numbers, sep='\t')
