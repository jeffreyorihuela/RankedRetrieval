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
            new_file.write(pair[0]+","+pair[1]+'\n')
        new_file.close()

class BlockedSortedBasedIndex:

    folder_path = ""
    blocks = 0
    mystopwords = stopwords.words('spanish')
    stemmer = SnowballStemmer('spanish')
    doc_name = ""
    size_block = 7000
    total_tweets = 0

    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.blocks += 1
        self.block = Block(self.size_block, str(self.blocks))
        self.mystopwords.append("https")

    def construction(self):
        with os.scandir(self.folder_path) as documents:
            for doc in documents:
                self.doc_name = doc.name
                print(doc.name)
                with open(self.folder_path+doc.name, "r", encoding="UTF-8") as file:
                    self.indexing(file)
        file = open('totaltweets.txt', 'w')
        file.write(str(self.total_tweets))
        file.close()
                    
    def merge_blocks(self):
        merged = 0
        path = 'blocks/'
        files = os.listdir(path)
        while len(files) > 1:
            for i in range(0, int(len(files) / 2)):
                merged+=1
                new_file = open(path+'file'+str(merged)+'.txt', 'w')
                self.merge(path+files[i*2], path+files[i*2+1], new_file)
                os.remove(path+files[i*2])
                os.remove(path+files[i*2+1])
            files = os.listdir(path)

    def merge(self, block1, block2, new_file):
        block1 = open(block1, 'r')
        block2 = open(block2, 'r')
        line_a = block1.readline()
        line_b = block2.readline()
        dictionary = {}
        while line_a or line_b:
            if line_a:
                self.merge_term(line_a, dictionary)
                line_a = block1.readline()
            if line_b:
                self.merge_term(line_b, dictionary)
                line_b = block2.readline()
        block1.close()
        block2.close()
        self.write_new_block(new_file, dictionary)
        new_file.close()

    def merge_term(self, line, dictionary):
        line = line.split(',')
        term = line[0]
        for i in line[1:]:
            if term not in dictionary:
                dictionary[term] = []
            dictionary[term].append(i)

    def write_new_block(self, new_file, dictionary):
        dictionary = dict(sorted(dictionary.items(), key=lambda item: item[0]))
        for term_id,docs in dictionary.items():
            new_line = term_id+','
            for doc_id in docs[:-1]:
                doc_id = doc_id.replace('\n','')
                new_line += (doc_id + ',')
            new_line += docs[-1]
            new_file.write(new_line)

    def indexing(self, file):
        text = file.read()
        json_text = json.loads(text)
        self.work_tweets(json_text)
        

    def work_tweets(self, json_text):
        for tweet in json_text:
            if tweet["retweeted"] == True:
                continue
            self.total_tweets += 1
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