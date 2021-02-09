#!/usr/bin/env python3

import json
import vocab

def total_amount(word, tale):
    amount = tale.count(word)
    amount_normalized = amount / len(tale)

    return amount_normalized

def term_frequency(book, vocab):
    # the amount of times that term t occurs in document d
    # normalized by the total amount of occurrences in document d
    tf = {}
    for voc in vocab:
        tf[voc] = {tale: total_amount(voc, tale) for tale in book}

    return tf

def inverse_document_frequency(book):
    # total amount of documents divided by
    # how many times the term t occurs in the set of documents d
    idf = {}
    for tale in book:
        idf[tale] =2


if __name__ == '__main__':
    with open('text_processed.json', 'r') as openfile:  # loading created json file
        book = json.load(openfile)

    book = book['book_lemmas']
    vocab = vocab.generate_vocab(book)
    tf = term_frequency(book, vocab[0])
    #idf = inverse_document_frequency(book)
    print(tf)
    #print(idf)
