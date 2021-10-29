#!/usr/bin/env python
# -*- coding: utf-8 -*-


def inverted_index_map(lines):
    for i, line in enumerate(lines, 1):
        for word in line.split():
            yield word, i


if __name__ == '__main__':
    import fileinput
    for word, line_no in inverted_index_map(fileinput.input()):
        print(word, line_no)
