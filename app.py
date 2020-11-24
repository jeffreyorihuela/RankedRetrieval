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
from flask import request
from flask import abort
from flask import jsonify


total_tweet = preproces()
#build()
#make_vectors(total_tweet=total_tweet)

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    
    if not request.json or not 'search' in request.json:
        abort(400)
    
    words = {}
    with open("mostfrequentwords.json", "r", encoding="UTF-8") as file:
        text = file.read()
        words = json.loads(text)
    stemmer = SnowballStemmer('spanish')
    mystopwords = stopwords.words('spanish')
    mystopwords.append('https')
    tokenized = nltk.word_tokenize(request.json['search'],'spanish')
    tokenized = [word for word in tokenized if word.isalpha()]
    tweet_words = []
    inverted_index = {}
    for token in tokenized:
        token = token.lower()
        token = stemmer.stem(token)
        if token in words:
            tweet_words.append(token)
            if token in inverted_index:
                inverted_index[token] += 1
            else:
                inverted_index[token] = 1

    vec = []
    for key in words:
        if key in tweet_words:
            with open("indexes/"+key+".json", "r",  encoding="UTF-8") as indexfile:
                index_text = indexfile.read()
                index_json = json.loads(index_text)
                T = len(tweet_words)
                F = inverted_index[key]
                TW = total_tweet
                WT = len(index_json)
                TF_IDF = round(F/T * math.log(TW/WT),2)
                vec.append(TF_IDF)
        else:
            vec.append(0)

    max_cosine = 0
    tweet_id = ""
    doc_name = ""

    with open("vectors/vec.csv", "r", encoding="UTF-8") as file:
        reader = csv.reader(file)
        
        row_count = 0
        for row in reader:
            if row_count == 0:
                #ignore headers
                row_count += 1
            else:
                tweet_data = row[:2]
                tweet_vect = row[2:]
                c = 0
                for i in range(len(tweet_vect)):
                    tweet_vect[i] = float(tweet_vect[i])
                    c+= tweet_vect[i]*vec[i]
                norm = float((sum(tweet_vect)*sum(vec))**0.5)
                if norm == 0:
                    cosine = 0
                else:
                    cosine = c / float((sum(tweet_vect)*sum(vec))**0.5)
                if cosine > max_cosine:
                    max_cosine = cosine
                    doc_name = tweet_data[0]
                    tweet_id = tweet_data[1]
    
    found = ""
    with open("data/"+doc_name, "r", encoding="UTF-8") as file:
        text = file.read()
        tweets = json.loads(text)
        
        for tweet in tweets:
            if str(tweet['id']) == str(tweet_id):
                if tweet['retweeted'] == True:
                    found = tweet['RT_text']
                else:
                    found = tweet['text'] 
                    print(tweet['text'])
        

    return jsonify({'tweet': found})