import json
import nltk

with open("data/tweets_2018-08-07.json", "r", encoding="UTF8") as f:
    text = f.read()
    decoded = json.loads(text)

for tweet in decoded:
    if tweet["retweeted"] == True:
        #print(tweet["user_name"],"retweeted: ", tweet["RT_text"])
        #print("from: ",tweet["RT_user_name"])
        print(nltk.word_tokenize(tweet["RT_text"], "spanish"))
    else:
        #print(tweet["user_name"],"says: ", tweet["text"])
        print(nltk.word_tokenize(tweet["text"]), "spanish")
