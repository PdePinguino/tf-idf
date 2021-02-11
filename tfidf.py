#!/usr/bin/env python3

import json
import math
import operator
import numpy as np
import vocab
import preprocessing

def frequency(term, tale):
    freq = tale.count(term)
    freq_normalized = freq / len(tale)

    return freq_normalized

def term_in_doc(term, doc):
    if term in doc:
        return 1
    else:
        return 0

def frequency_N(term, book):
    # number of documents that term t occurs in book (set of documents)
    freq = 0
    for tale in book:
        freq += term_in_doc(term, book[tale])
    #print(freq, term)
    if freq < 1:
        raise ValueError('no terms should appear in no documents')

    return freq

def TF(book, vocab):
    # Term Frequency
    # the amount of times that term t occurs in document d
    # normalized by the total amount of occurrences in document d
    tf = {}
    for voc in vocab:
        tf[voc] = {tale: frequency(voc, book[tale]) for tale in book}

    check_tf(tf)

    return tf

def IDF(book, vocab):
    # Inverse Document Frequency
    # total amount of documents d divided by
    # the number of documents d in which the term t occurs
    idf = {}
    N = len(book.keys())

    for voc in vocab:
        # added 1 to denominator to avoid division by 0 if term t is not in any document
        idf_score = math.log(N / frequency_N(voc, book) + 1)
        # if term t appears in all documents, then log is 0.0
        if idf_score == 0.0:  # smoothing idf score to avoid multiplication by 0
            idf_score = 0.0000001
        idf[voc] = idf_score

    check_idf(idf)

    return idf

def check_tf(tf):
    # checking that the tf_score across all documents is greater than 0.0
    for tale in tf:
        tf_score = [tf[tale][t] for t in tf[tale]]
        if sum(tf_score) == 0.0:
            raise ValueError(tf_score)

def check_idf(idf):
    for t in idf:
        if idf[t] == 0:
            print(idf[t])
            raise ValueError()

def TFIDF(tf, idf, vocab):
    tf_idf = {}
    for title in book:
        tf_idf[title] = {}
        for voc in vocab:
            tf_idf[title][voc] = tf[voc][title] * idf[voc]

    return tf_idf

def tfidf_print(tf_idf):
    for title in tf_idf:
        print(title)
        for voc in tf_idf[title]:
            print('\t',voc, tf_idf[title][voc])

def matching_score(tf_idf, query):
    # input: query as a string (i.e. 'this is a query')
    query_preprocessed = preprocessing.preprocess_query(query)
    matching_score = {title: 0 for title in tf_idf.keys()}

    for term in query_preprocessed:
        for title in tf_idf:
            if term in tf_idf[title]:
                matching_score[title] += tf_idf[title][term]

    best_k = rank_scores(matching_score, k=10)

    return best_k

def rank_scores(scores, k=-1):
    if k == -1: k = len(scores)
    ranked_scores = {k: v for k, v in sorted(scores.items(), key=operator.itemgetter(1), reverse=True)[:k]}

    return ranked_scores

def vocab2index(vocab):
    v2i = {voc: index for index, voc in enumerate(vocab)}
    print(v2i)
    return v2i

def vectorize_tfidf(v2i, tfidf):
    vector = np.zeros(len(v2i))
    for voc in v2i:
        index = v2i[voc]
        vector[index] = tfidf[voc]

    return vector

def vectorize_query(query):
    # input: query as a string (i.e. 'this is a query')
    query_preprocessed = preprocessing.preprocess_query(query)
    # obtaining tf-idf for query
    


if __name__ == '__main__':
    with open('text_processed.json', 'r') as openfile:  # loading created json file
        book = json.load(openfile)

    book = book['book_lemmas']
    book = {'1':['hola','cómo','estás', 'yo'], '2':['bien','y','tu', 'yo'], '3':['hola','hola','bien']}
    vocab = vocab.generate_vocab(book)
    vocab = list(vocab[0])

    tf = TF(book, vocab)
    idf = IDF(book, vocab)

    tf_idf = TFIDF(tf, idf, vocab)
    tfidf_print(tf_idf)

    matching_score(tf_idf, query='hola cómo estás?')

    # Document Vectorization
    v2i = vocab2index(vocab)
    documents_vectors = {tale: vectorize_tfidf(v2i, tf_idf[tale]) for tale in book}
    #for k,v in documents_vectors.items():
    #    print(k,v)
