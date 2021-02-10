#!/usr/bin/env python3

import json
import vocab

def frequency(word, tale):
    freq = tale.count(word)
    freq_normalized = freq / len(tale)

    return freq_normalized

def frequency_N(word, book):
    freq = 0
    for tale in book:
        freq += book[tale].count(word)

    return freq

def term_frequency(book, vocab):
    # the amount of times that term t occurs in document d
    # normalized by the total amount of occurrences in document d
    tf = {}
    for voc in vocab:
        tf[voc] = {tale: frequency(voc, book[tale]) for tale in book}

    check_tf(tf)

    return tf

def inverse_document_frequency(book, vocab):
    # total amount of documents d divided by
    # the number of documents d that the term t occurs
    idf = {}
    N = len(book.keys())
    for voc in vocab:
        idf[voc] = frequency_N(voc, book)

    check_idf(idf)

    return idf

def check_tf(tf):
    for t in tf:
        z = [tf[t][tale] for tale in tf[t]]
        if sum(z) == 0.0:
            print(tf[t][tale])
            raise ValueError()

def check_idf(idf):
    for t in idf:
        if idf[t] == 0:
            print(idf[t])
            raise ValueError()

if __name__ == '__main__':
    with open('text_processed.json', 'r') as openfile:  # loading created json file
        book = json.load(openfile)

    book = book['book_lemmas']
    vocab = vocab.generate_vocab(book)
    tf = term_frequency(book, vocab[0])
    idf = inverse_document_frequency(book, vocab[0])
