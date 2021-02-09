#!/usr/bin/env python3

import json

def generate_vocab(book):
    if isinstance(book[list(book.keys())[0]], str):
        vocab = [token for tale in book for token in book[tale].split()]
    else:
        vocab = [token for tale in book for token in book[tale]]

    vocab = (set(vocab), len(set(vocab)), len(vocab))
    # vocab = tuple with types, total number of types, and total number of tokens
    return vocab


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
