#!/usr/bin/env python3

import re
import spacy
import json
from PyPDF2 import PdfFileReader


def is_title(text):
    # if a page has less than 15 words, it is a title
    if len(text.split()) < 15:
        return True
    else:
        return False

def extract_tales(file):
    book = {}
    with open(file, 'rb') as f:  # pdf has to be read in 'rb' mode
        pdf = PdfFileReader(f)  # pdf manager
        number_of_pages = pdf.getNumPages()

        # traversing pdf pages and getting text
        for i in range(number_of_pages):
            page = pdf.getPage(i)
            text = page.extractText()
            if is_title(text):  # checking if page is a new title, thus a different tale
                title = ' '.join(text.split())
                book[title] = []  # each tale is a new dictionary entry
            try:
                book[title].append(text)
            except UnboundLocalError:
                pass

    return book

def remove_punctuation(tale):
    punctuation = re.compile(r'[!¡"#$%&(),\*+-\./\:;<=>¿?@\[\]^_`{}~|]')
    tale = [re.sub(punctuation, '', tale[line]) for line in range(len(tale))]

    return tale

def remove_ool_characters(tale):
    ool_chars = re.compile(r'[Šﬁ]')
    tale = [re.sub(ool_chars, '', tale[line]) for line in range(len(tale))]
    return tale

def remove_whitespace(tale):
    tale = [' '.join(tale[page].split()) for page in range(len(tale))]
    return tale

def lowercase(tale):
    tale = [word.lower() for word in tale]

    return tale

def join_pages(tale):
    tale = ' '.join([page for page in tale[1:]])  # dropping first line that is the title
    return tale

def clean_tale(tale):
    tale = remove_punctuation(tale)
    tale = remove_ool_characters(tale)
    tale = remove_whitespace(tale)
    tale = lowercase(tale)
    tale = join_pages(tale)  # each page is a string in tale; now is only one long string

    return tale

def clean_book(book):
    for tale in book.keys():
        book[tale] = clean_tale(book[tale])

    return book

def lemmatize(book):
    nlp = spacy.load('es_dep_news_trf')
    lemmas = {}
    for tale in book:
        doc = nlp(book[tale])
        lemmas[tale] = [token.lemma_ for token in doc]

    return lemmas

def preprocess(file):
    book = extract_tales(file)
    book = clean_book(book)
    book_lemmas = lemmatize(book)
    print(book.keys(), book_lemmas.keys())
    return book, book_lemmas


if __name__ == '__main__':

    file = 'cuentos-manuel-rojas.pdf'
    book, book_lemmas = preprocess(file)  # book is a dictionary with each tale's title as key
    # book[title] is a long string with the tale.
    print(f'tale\'s titles: {list(book.keys())}')
    print(f'number of tales: {len(book.keys())}')
    title = list(book.keys())[0]
    print(f'excerpt of tale {title}:\n{book[title][:100]}...')
    print(f'type: {type(book[title])}')
    print(f'excerpt of tale lemmatized {title}:\n{book_lemmas[title][:100]}...')
    print(f'type: {type(book_lemmas[title])}')
    
    # to sabe to json format, uncomment these lines
    #object = {'book': book, 'book_lemmas': book_lemmas}
    #with open('text_processed2.json', 'w', encoding='utf8') as outfile:
    #    json.dump(object, outfile)
