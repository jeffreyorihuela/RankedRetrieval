import json
import os
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

def build():

    file = "mostfrequentwords.json"

    words = {}

    with open(file, "r", encoding="UTF-8") as f:
        text = f.read()
        words = json.loads(text)

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
                    
                    for word in tokenized:
                        word = word.lower()
                        word = stemmer.stem(word)
                        if word in words:
                            if  os.path.isfile('./indexes/'+word+'.json'):
                                #modify index
                                index_str = ""
                                with open('indexes/'+word+'.json', 'r', encoding="UTF-8") as f:
                                    index_data = f.read()
                                    index_json = json.loads(index_data)
                                    
                                    id_key = str(tweet['id'])
                                    if id_key in index_json:
                                        index_json[id_key] += 1
                                    else:
                                        index_json[tweet['id']] = 1
                                    index_str = json.dumps(index_json, indent=4, ensure_ascii=False)

                                with open('indexes/'+word+'.json', 'w', encoding="UTF-8") as f:
                                    f.write(index_str)
                            else:
                                #create index
                                index_json = {
                                    tweet['id']: 1
                                }
                                index_json = json.dumps(index_json, indent=4, ensure_ascii=False)
                                with open('indexes/'+word+'.json', 'a+', encoding="UTF-8") as f:
                                    f.write(index_json)
                            
