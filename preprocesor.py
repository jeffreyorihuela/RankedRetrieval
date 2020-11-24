import json
import nltk
import os
import operator

from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

#return number of tweets

def preproces():
    lexicon = {}
    total_tweets = 0
    basepath="data/"
    with os.scandir(basepath) as entries:
        for entry in entries:
            with open(basepath +entry.name, "r", encoding="UTF8") as f:
                text = f.read()
                decoded = json.loads(text)
                stemmer = SnowballStemmer('spanish')
                mystopwords = stopwords.words('spanish')
                mystopwords.append("https")
                tokenized = []

                for tweet in decoded:
                    total_tweets += 1
                    #print(type(tweet["id"]))
                    if tweet["retweeted"] == True:
                        #print(tweet["user_name"],"retweeted: ", tweet["RT_text"])
                        #print("from: ",tweet["RT_user_name"])
                        #print(nltk.word_tokenize(tweet["RT_text"], "spanish"))
                        tokenized = nltk.word_tokenize(tweet["RT_text"], "spanish")
                    else:
                        #print(tweet["user_name"],"says: ", tweet["text"])
                        #print(nltk.word_tokenize(tweet["text"], "spanish"))
                        tokenized = nltk.word_tokenize(tweet["text"], "spanish")
                    tokenized = [word for word in tokenized if word.isalpha()]
                    for word in tokenized:
                        word = word.lower()
                        if word not in mystopwords:
                            word = stemmer.stem(word)
                            if word in lexicon:
                                lexicon[word] = lexicon[word]+1
                            else:
                                lexicon[word] = 1

    sorted_lexicon = dict(sorted(lexicon.items(), key=lambda kv: kv[1], reverse=True))

    max_size = 50

    if len(sorted_lexicon) > max_size:
        elements_to_del = len(sorted_lexicon) - max_size
        for _ in range(elements_to_del):
            sorted_lexicon.popitem()


    json_object = json.dumps(sorted_lexicon, indent=4, ensure_ascii=False)
    with open("mostfrequentwords.json", "w") as outfile:
        outfile.write(json_object)

    return total_tweets