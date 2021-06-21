import nltk
import json
import os
import math
import csv

from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from preprocesor import preproces
from tfidf import make_vectors
from indexbuilder import build
from flask import Flask
from flask_cors import cross_origin
from flask import request
from flask import abort
from flask import jsonify


bsbi = BlockedSortedBasedIndex("data/")
bsbi.construction()
bsbi.merge_blocks()

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
    
    request.json['search']

    
        

    return jsonify({'tweet': found})