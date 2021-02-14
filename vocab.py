#!/usr/bin/env python3

import json
import operator
from nltk.corpus import stopwords


def generate_vocab(book):
    if isinstance(book[list(book.keys())[0]], str):
        vocab = [token for tale in book for token in book[tale].split()]
    else:
        vocab = [token for tale in book for token in book[tale]]

    vocab = (set(vocab), len(set(vocab)), len(vocab))
    # vocab = tuple with types, total number of types, and total number of tokens
    return vocab

def frequency_document(book):
    freq = {}
    for word in book:
        try:
            freq[word] += 1
        except KeyError:
            freq[word] = 1

    ranked_freq = {k: v for k, v in sorted(freq.items(), key=operator.itemgetter(1), reverse=True)}

    return ranked_freq

def frequency_book(book):
    freq_book = {tale: frequency_document(book[tale]) for tale in book}

    return freq_book

def print_freq_book(freq_book, n=10, stopwords=False):
    for tale in freq_book:
        print(tale)
        if stopwords:
            words = [(word, freq_book[tale][word]) for word in freq_book[tale] if word not in stopwords]
        else:
            words = [(word, freq_book[tale][word]) for word in freq_book[tale]]

        print(words[:n])


if __name__ == '__main__':
    with open('text_processed.json', 'r') as openfile:  # loading created json file
        book = json.load(openfile)
    # book is a dictionary with raw and lemmatized books
    # book['book'] - book['book_lemmas']
    # both objects are nested dictionaries with tale's titles as keys.
    # i.e. book['book_lemmas']['EL DELINCUENTE']

    vocab = generate_vocab(book['book_lemmas'])
    print(f'total number of types in book: {vocab[1]}')
    print(f'total number of tokens in book: {vocab[2]}')
    print(f'10 types from vocab: {list(vocab[0])[:10]}')

    freq_book = frequency_book(book['book_lemmas'])
    # stopwords.words('spanish')
    print_freq_book(freq_book, n= 10, stopwords=False)
