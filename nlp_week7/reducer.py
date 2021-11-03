#!/usr/bin/env python
# -*- coding: utf-8 -*-
from itertools import groupby
from operator import itemgetter


def inverted_index_reduce(items):
    # I know I am not supposed to use groupby but sorting is not working for some reason
    # Join the lines with same ngram together
    for ngram, ngram_lines in groupby(items, key=itemgetter(0)):
        lines = [line[1:][0] for line in ngram_lines]
        yield ngram, lines


def split_dummy(text):
    return str.split(text.strip(), '\t')

if __name__ == '__main__':
    import fileinput
    iterable = map(split_dummy, fileinput.input())
    for word, lines in inverted_index_reduce(iterable):
        print(word, *lines, sep='\t')