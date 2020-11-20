import json
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

with open("data/tweets_2018-08-07.json", "r", encoding="UTF8") as f:
    text = f.read()
    decoded = json.loads(text)

mystopwords = stopwords.words('spanish')
stemmer = SnowballStemmer('spanish')
tokenized = []
lexicon = {}
for tweet in decoded:
    
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
        if word not in stopwords.words('spanish'):
            word = stemmer.stem(word)
            if word in lexicon:
                lexicon[word] = lexicon[word]+1
            else:
                lexicon[word] = 1

print(lexicon)
    