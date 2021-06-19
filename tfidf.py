import os
import json
import csv
import nltk
import math
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer


#TF frecuencia del termino en un documento log ( 1 + TF)
#IDF  log (total de documentos / frecuencia en coleccion)

def make_vectors(total_tweet):

    words = {}

    with open("mostfrequentwords.json", "r", encoding="UTF-8") as f:
        text = f.read()
        words = json.loads(text)


    with open("vectors/vec.csv", "w", newline='') as output_file:
        writer = csv.writer(output_file)
        headers=["filename","id"]
        for key in words:
            headers.append(key)
        writer.writerow(headers)
        basepath = "data/"
        with os.scandir(basepath) as entries:
            for entry in entries:
                with open(basepath+entry.name, "r", encoding="UTF-8") as file:
                    text = file.read()
                    json_file = json.loads(text)
                    stemmer = SnowballStemmer('spanish')
                    mystopwords = stopwords.words('spanish')
                    mystopwords.append("https")
                    for tweet in json_file:
                        if tweet["retweeted"] == True:
                            tokenized = nltk.word_tokenize(tweet["RT_text"], "spanish")
                        else :
                            tokenized = nltk.word_tokenize(tweet["text"], "spanish")
                        tokenized = [word for word in tokenized if word.isalpha()]
                        tweet_words = []
                        for token in tokenized:
                            token = token.lower()
                            token = stemmer.stem(token)
                            if token in words:
                                tweet_words.append(token)
                        tweet_id = str(tweet['id'])
                        vec = []
                        vec.append(entry.name)
                        vec.append(tweet_id)
                        for key in words:
                            if key in tweet_words:
                                with open("indexes/"+key+".json", "r",  encoding="UTF-8") as indexfile:
                                    index_text = indexfile.read()
                                    index_json = json.loads(index_text)
                                    T = len(tweet_words)
                                    F = index_json[tweet_id]
                                    TW = total_tweet
                                    WT = len(index_json)
                                    TF_IDF = round(F/T * math.log(TW/WT),2)
                                    vec.append(TF_IDF)
                            else:
                                vec.append(0)
                        writer.writerow(vec)

