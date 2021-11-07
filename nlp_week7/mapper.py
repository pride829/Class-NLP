#!/usr/bin/env python
# -*- coding: utf-8 -*-


def expander(words):
    # expander expande the n-word pharse to a 2^n-1 set that contains all kind of combination except the one with all '-' 
    if len(words) == 1:
        return [[words[0]], ['_']]

    output = []
    for w in expander(words[1:]):
        output += [[words[0]] + w]
        output += [['_'] + w]

    return output

def inverted_index_map(lines):
    # split the line and call expander
    for i, line in enumerate(lines, 1):
        line = line.strip()
        ngram, ngramcounts = line.split('\t')
        words = ngram.split()
        for c in expander(words)[:-1]:
            print(' '.join(c) + '\t' + line.replace('\t', ' '))


    return

if __name__ == '__main__':
    import fileinput
    inverted_index_map(fileinput.input())
    
    # the codes are kind of shitty but I am too tired to care
