import nltk
import json
import os
import math
import csv

from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from tfidf import tf_idf
from tfidf import tf
from BSBI import BlockedSortedBasedIndex
from flask import Flask
from flask_cors import cross_origin
from flask import request
from flask import abort
from flask import jsonify


bsbi = BlockedSortedBasedIndex("data/")
bsbi.construction()
bsbi.merge_blocks()
tf_idf()

app = Flask(__name__)

@app.route('/', methods=['GET'])
@cross_origin()
def words():
    words = {}
    with open("mostfrequentwords.json", "r", encoding="UTF-8") as file:
        text = file.read()
        words = json.loads(text)

    return words

@app.route('/', methods=['POST'])
@cross_origin()
def indexing():
    
    if not request.json or not 'search' in request.json:
        abort(400)

    mystopwords = stopwords.words('spanish')
    stemmer = SnowballStemmer('spanish')
    
    query = request.json['search']
    
    tokens = nltk.word_tokenize(query, 'spanish')
    tokens = [token.lower() for token in tokens if token.isalpha()]
    tokens = [stemmer.stem(token) for token in tokens if token not in mystopwords]


    print(tokens)
    #vectorizamos la query
    tf_query = {}
    for token in tokens:
        if token not in tf_query:
            tf_query[token] = 0
        tf_query[token] += 1
    
    for key, value in tf_query.items():
        tf_query[key] = tf(value)
    
    print(tf_query)

    scores = {}

    with open('weightmatrix.txt', 'r', encoding='UTF-8') as file:
        line = file.readline()
        while line:
            line = line.split(',')
            term = line[0]
            if term not in tokens:
                line = file.readline()
                continue
            idf = line[-1].split(':')[1]
            idf = float(idf.replace('\n', ''))
            for doc_id in line[1:-1]:
                splitt = doc_id.split('=')
                doc_id = splitt[0]
                tf_doc = float(splitt[1])
                if doc_id not in scores:
                    scores[doc_id] = 0
                scores[doc_id] += (tf_doc * idf * tf_query[term] * idf)

            line = file.readline()

    scores = dict(sorted(scores.items(), key=lambda item: item[1]))
    if len(scores) <= 5:
        return jsonify(scores)
    else:
        return jsonify(dict(list(scores.items())[-5:]))
    