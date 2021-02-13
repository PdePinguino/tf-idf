#!/usr/bin/env python3

import json
import math
import operator
import argparse
import numpy as np
import vocab
import preprocessing
import plot


class TFIDF():
    def __init__(self, documents, vocab):
        self.documents = documents
        self.vocab = vocab
        self.N = len(documents)

    def frequency(self, term, document):
        """
        returns the normalized frequency of term t in document d
        """
        freq = document.count(term)
        freq_normalized = freq / len(document)

        return freq_normalized

    def frequency_N(self, term):
        """
        returns the number of documents that term t occurs in
        """
        freq = 0
        for doc in self.documents:
            if term in self.documents[doc]:
                freq += 1

        return freq

    def compute_tf(self, document):
        """
        function that computes the term frequency for all vocabulary:
        the amount of times that term t occurs in document d
        normalized by the total amount of occurrences in document d
        """
        tf = {voc: self.frequency(voc, document) for voc in self.vocab}

        return tf

    def compute_idf(self):
        """
        function that computes the inverse document frequency:
        total amount of documents d divided by
        the number of documents d in which the term t occurs
        """
        idf = {}
        for voc in self.vocab:
            # added 1 to numerator to avoid negative values
            # added 1 to denominator to avoid division by 0 if term t is not in any document
            df = self.frequency_N(voc)
            idf_score = math.log((self.N + 1) / (df + 1))
            #print(voc, 'df', df, 'idf_score', idf_score)
            # if term t appears in all documents: log(N/N) --> log(1) --> idf =  0.0
            # smoothing idf score to avoid multiplication by 0
            if idf_score == 0.0:
                idf_score = 0.0000001

            idf[voc] = idf_score
        print(idf)
        return idf

    def compute_tfidf(self, tf, idf):
        """
        function that computes tf-idf score:
        tf is passed as a dictionary with tf values per word in vocabulary for a specific document.
        idf is a dictionary with idf values per word in vocabulary.
        """
        tfidf_score = {voc: tf[voc] * idf[voc] for voc in self.vocab}

        return tfidf_score

    def query2tfidf(self, query):
        """
        function that computes tf-idf for query
        input: query preprocessed
        output: tfidf for query
        """
        tf = self.compute_tf(query)
        idf = self.compute_idf()
        tfidf_query = self.compute_tfidf(tf, idf)

        return tfidf_query

    def matching_score(self, tfidf_documents, query):
        """
        function that matches query to all documents
        and assigns a score for each.
        the score is calculated regarding the tfidf value per word in the document
        input: tfidf for each document and query preprocessed
        output: a dictionary with ordered results by their matching score
        """
        matching_score = {doc: 0 for doc in tfidf_documents}

        for term in query:
            for doc in tfidf_documents:
                if term in tfidf_documents[doc]:
                    matching_score[doc] += tfidf_documents[doc][term]

        best_k = self.rank_scores(matching_score, k=10)

        return best_k

    def rank_scores(self, scores, k=-1):
        """
        function that ranks (descending order) score results
        input: scores is a dictionary, k is the amount of results to retrieve
        output: ranked scores dictionary with a max lenght of k
        if k == -1, then all results are retrieved
        """
        if k == -1: k = len(scores)
        ranked_scores = {k: v for k, v in sorted(scores.items(), key=operator.itemgetter(1), reverse=True)[:k]}

        return ranked_scores

    def vectorize_tfidf(self, tfidf):
        """
        function that converts the tfidf dictionary to vector space (numpy array)
        each word's value is stored in its index position
        """
        vector = np.zeros(len(self.vocab))
        for voc in self.vocab:
            index = self.vocab.index(voc)
            vector[index] = tfidf[voc]

        return vector

    def cosine_similarity(self, v1, v2):
        """
        function that computes the cosine similarity between two vectors
        """
        cos_sim = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

        return cos_sim


if __name__ == '__main__':
    def tfidf_print(tf_idf):
        for title in tf_idf:
            print(title)
            for voc in tf_idf[title]:
                print('\t',voc, tf_idf[title][voc])

    parser = argparse.ArgumentParser(description='...')
    parser.add_argument('-t', '--test', action='store_true', default=False)
    args = parser.parse_args()

    if args.test:
        documents = {'1':['hola','cómo','estás'], '2':['hola', 'y','tu', 'yo'], '3':['bien', 'cómo', 'estás']}
        query = 'hola cómo estás? yo'
        print(documents)
        print(query)
    else:
        with open('text_processed.json', 'r') as openfile:  # loading created json file
            book = json.load(openfile)
        documents = book['book_lemmas']
        query = ' '.join(['pedir', 'su', 'desayuno', 'temprano', 'pagar', 'su', 'cuenta', 'y', 'él', 'marchar', 'este', 'ser', 'todo', 'el', 'historia', 'uno', 'momento', 'de', 'silencio', 'y', 'no', 'él', 'ver', 'más', 'preguntar', 'dos', 'o', 'tres', 'voz', 'a', 'uno', 'tiempo', 'nunca', 'más', 'él', 'sentir', 'varios', 'puñetazo', 'sobre', 'el', 'mesa'])

    vocab = vocab.generate_vocab(documents)
    vocab = list(vocab[0])
    tfidf = TFIDF(documents, vocab)

    tf_documents = {doc: tfidf.compute_tf(documents[doc]) for doc in documents}
    # tf_documents is a dictionary to store each word's tf value per document.
    # tf_documents['doc']['word'] = tf_score

    idf = tfidf.compute_idf()
    # idf is a dictionary to store each word's idf value.
    # as opposed to tf, idf is a unique value per word across the corpus.
    # idf['word'] = idf_score

    tfidf_documents = {doc: tfidf.compute_tfidf(tf_documents[doc], idf) for doc in documents}
    #tfidf_print(tfidf_documents)

    # input: query as a string (i.e. 'this is a query')
    query_preprocessed = preprocessing.preprocess_query(query)

    best_k = tfidf.matching_score(tfidf_documents, query_preprocessed)
    for k,v in best_k.items():
        print(k,v)

    query_tfidf = tfidf.query2tfidf(query_preprocessed)
    query_vector = tfidf.vectorize_tfidf(query_tfidf)
    documents_vectors = {doc: tfidf.vectorize_tfidf(tfidf_documents[doc]) for doc in tfidf_documents}

    cosine_similarities = {document: tfidf.cosine_similarity(documents_vectors[document], query_vector) for document in documents_vectors}

    sorted_cosine_similarities = {k: v for k, v in sorted(cosine_similarities.items(), key=operator.itemgetter(1), reverse=True)}
    for k,v in sorted_cosine_similarities.items():
        print(k,'\t',v)
