import json
import os
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import time

class Block:
    entries = []
    def __init__(self, size, name):
        self.size = size
        self.name = name
        self.entries = []

    def add(self, term_id, doc_id):
        pair = (term_id, doc_id)
        self.entries.append(pair)

    def is_full(self):
        return len(self.entries) >= self.size
    
    def save_block(self):
        self.entries.sort(key = lambda tup: tup[0])
        new_file = open("blocks/"+self.name+".txt", "w")
        for pair in self.entries:
            new_file.write(pair[0]+","+pair[1]+"\n")
        new_file.close()

class BlockedSortedBasedIndex:

    folder_path = ""
    blocks = 0
    mystopwords = stopwords.words('spanish')
    stemmer = SnowballStemmer('spanish')
    doc_name = ""
    size_block = 7000

    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.blocks += 1
        self.block = Block(self.size_block, str(self.blocks))
        self.mystopwords.append("https")

    def construction(self):
        start = time.time()
        with os.scandir(self.folder_path) as documents:
            for doc in documents:
                self.doc_name = doc.name
                print(doc.name)
                with open(self.folder_path+doc.name, "r", encoding="UTF-8") as file:
                    self.indexing(file)
        end = time.time()
        print(end-start)

    def merge_blocks(self):
        merged = 0
        path = 'blocks/'
        files = os.listdir(path)
        while len(files) > 1:
            for i in range(0, int(len(files) / 2)):
                os.remove(path+files[i*2])
                os.remove(path+files[i*2+1])
                merged+=1
                new_file = open(path+'file'+str(merged)+'.txt', 'w')
                new_file.write('ga')
                new_file.close()
            files = os.listdir(path)

    def indexing(self, file):
        text = file.read()
        json_text = json.loads(text)
        self.work_tweets(json_text)
        

    def work_tweets(self, json_text):
        for tweet in json_text:
            if tweet["retweeted"] == True:
                continue
            tokens = self.tokenize(tweet)
            for token in tokens:
                token = token.lower()
                if token not in self.mystopwords:
                    token = self.stemmer.stem(token)
                    if self.block.is_full():
                        #guardar bloque en disco
                        self.block.save_block()
                        self.blocks += 1
                        #crear nuevo bloque
                        self.block = Block(self.size_block, str(self.blocks))
                    else:
                        self.block.add(token, self.doc_name+":"+str(tweet['id']))
        self.block.save_block()

    def tokenize(self, tweet):
        tokenized = nltk.word_tokenize(tweet["text"], "spanish")
        return [word for word in tokenized if word.isalpha()]

                            
bsbi = BlockedSortedBasedIndex("data/")
bsbi.construction()
bsbi.merge_blocks()