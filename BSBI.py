import json
import os
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

class Block:
    entries = []
    def __init__(self, size):
        self.size = size

    def add(self, term_id, doc_id):
        pair = (term_id, doc_id)
        self.entries.append(pair)

    def is_full(self):
        return len(self.entries) >= self.size
    


class BlockedSortedBasedIndex:

    folder_path = ""
    blocks = []
    mystopwords = stopwords.words('spanish')
    stemmer = SnowballStemmer('spanish')
    doc_name = ""

    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.block = Block(5000)
        self.mystopwords.append("https")

    def construction(self):
        with os.scandir(self.folder_path) as documents:
            for doc in documents:
                self.doc_name = doc.name
                with open(self.folder_path+doc.name, "r", encoding="UTF-8") as file:
                    self.indexing(file)

    #def mergeBlocks():
        

    def indexing(self, file):
        text = file.read()
        json_text = json.loads(text)
        self.work_tweets(json_text)
        

    def work_tweets(self, json_text):
        for tweet in json_text:
            tokens = self.tokenize(tweet)
            for token in tokens:
                token = token.lower()
                if token not in self.mystopwords:
                    token = self.stemmer.stem(token)
                    if self.block.is_full():
                        #guardar bloque en disco
                        #crear nuevo bloque
                        print("TODO")
                    else:
                        self.block.add(token, self.doc_name+":"+str(tweet['id']))

    def tokenize(self, tweet):
        if tweet["retweeted"] == True:
            tokenized = nltk.word_tokenize(tweet["RT_text"], "spanish")
        else :
            tokenized = nltk.word_tokenize(tweet["text"], "spanish")
        return [word for word in tokenized if word.isalpha()]

                            
bsbi = BlockedSortedBasedIndex("data/")
bsbi.construction()