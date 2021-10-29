#!/usr/bin/env python
# -*- coding: utf-8 -*-
from operator import itemgetter, xor
from itertools import product
from heapq import nlargest
import logging


MAX_LEN = 5


def parse_ngramstr(text):
    # 將ngramcount拆成tuple
    ngram, count = text.rsplit(maxsplit=1)
    return ngram, int(count)


def parse_line(line):
    #將輸入拆成query和ngramcount
    query, *ngramcounts = line.strip().split('\t')

    #print(list(map(parse_ngramstr, ngramcounts)))
    # TODO: 了解：這裡的map會轉換成tuple物件?

    return query, tuple(map(parse_ngramstr, ngramcounts))


def expand_query(query, max_len):
    # TODO: write your query expansion, e.g.,
    #  "in/at afternoon" -> ["in afternoon", "at afternoon"]
    #  "listen ?to music" -> ["listen music", "listen to music"]

    queries = [query]

    flag = True
    while flag:
        flag = False
        for q in queries:
            words = q.split()
            for i in range(len(words)):
                if flag == True:
                    continue
                w = words[i]
                if '/' in w:
                    flag = True
                    word_a, word_b = w.split('/')
                    queries.append( ' '.join( words[:i] + [word_a] + words[i+1:] ) )
                    queries.append( ' '.join( words[:i] + [word_b] + words[i+1:] ) )
                    queries.remove(q)
                elif '?' in w:
                    flag = True
                    word = w.replace('?', '')
                    queries.append( ' '.join( words[:i] + [word] + words[i+1:] ) )
                    queries.append( ' '.join( words[:i] + words[i+1:] ) )
                    queries.remove(q)
                elif '*' == w:
                    flag = True
                    # Expand the query to the max length
                    for j in range(max_len - (len(words)-1) + 1):
                        queries.append( ' '.join( words[:i] +
                                        ['_' for k in range(0, j)] + 
                                        words[i+1:]
                                        ))
                    queries.remove(q)


    return queries


def extend_query(query):
    # TODO: write your query extension, 
    # e.g., can tolerate missing/unnecessary determiners
    return [query]


def load_data(lines):
    logging.info('Loading...', end='')
    # read linggle data
    # 讀取資料後轉換成tuple

    linggle_table = {query: ngramcounts for query, ngramcounts in map(parse_line, lines)}
    logging.info('ready.')
    return linggle_table


def linggle(linggle_table):
    q = input('linggle> ')

    # exit execution keyword: exit()
    if q == 'exit()':
        return

    #max_len = max([len(n.split()) for n in linggle_table])
    max_len = 5 # Pre-calculation show that it is 5

    # extend and expand query
    # TODO: 這裡的for看起來是由前往後執行？原來是這樣嗎？

    queries = [
        simple_query
        for query in extend_query(q)
        for simple_query in expand_query(query, 5)
    ]

    print(queries)
    # gather results
    # ngramcounts is a set
    ngramcounts =  {item 
                     for query in queries if query in linggle_table 
                     for item in linggle_table[query]}

    # output 10 most common ngrams
    ngramcounts = nlargest(10, ngramcounts, key=itemgetter(1))

    if len(ngramcounts) > 0:
        print(*(f"{count:>7,}: {ngram}" for ngram, count in ngramcounts), sep='\n')
    else:
        print(' '*8, 'no result.')
    print()

    return True


if __name__ == '__main__':
    import fileinput
    # If the readline module was loaded, then input() will use it to provide elaborate line editing and history features.
    # https://docs.python.org/3/library/functions.html#input
    import readline

    linggle_table = load_data(fileinput.input())
    
    while linggle(linggle_table):
        pass