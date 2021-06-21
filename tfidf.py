import os
import json
import csv
import nltk
import math

#TF frecuencia del termino en un documento log ( 1 + TF)
#IDF  log (total de documentos / frecuencia en coleccion)

def idf(n, doc_freq):
    return round(math.log(n/doc_freq), 4)

def tf(freq):
    return 1 + round(math.log(freq), 4)

def save_freq(term, d, tf_file, n):
    line = term + ','
    for key, value in d.items():
        value = tf(value)
        line += (key + '=' +str(value)+',')
    line += ('idf:'+ str(idf(n, len(d)))+'\n')
    tf_file.write(line)

def read_freq(line):
    dictionary = {}
    for i in line[1:]:
        i = i.replace('\n', '')
        if i not in dictionary:
            dictionary[i] = 0
        dictionary[i] += 1
    return dictionary

def count_freq(line, tf_file, n):
    line = line.split(',')
    term =  line[0]
    d = read_freq(line)
    save_freq(term, d, tf_file, n)

def tf_idf():
    files = os.listdir('blocks/')
    file = open('totaltweets.txt', 'r')
    n = file.readline()
    file.close()
    with open('blocks/'+files[0], 'r', encoding="UTF-8") as f:
        line = f.readline()
        tf_file = open('weightmatrix.txt', 'w')
        while line:
            count_freq(line, tf_file, int(n))
            line = f.readline()
        tf_file.close()

tf_idf()

