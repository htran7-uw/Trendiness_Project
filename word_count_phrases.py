import re
import pandas as pd
import numpy as np 
import argparse  

parser = argparse.ArgumentParser()
parser.add_argument('filename')
parser.add_argument('word',type=str,help='Display frequency of the user input')
parser.add_argument("flag", nargs="?", default=" ")
args = parser.parse_args()

final=[]
Phrase =[]

with open(args.filename) as file:
	lines = file.readlines()

tweets = pd.DataFrame(lines)
#print(tweets.shape)
#print(tweets[0][1])
tweets_empty = []
for i, words in enumerate(tweets[0]):
	if words == '':
		tweets_empty.append(i)
'''Check for empty lists'''
try:
	tweets.drop([tweets_empty],axis = 0, inplace=True)
except KeyError:
	Pass
tweets.dropna(inplace = True)

'''real phrases detecting'''
for i, text in enumerate(tweets[0]):
    doc = nlp(text.strip().lower())
    words = list()
    phrases = list()
    for r in doc.noun_chunks:
        if len(r.text.split(' ')) > 1:
             phrases.append(r.text)
        else:
             words.append(r.text.strip().lower())

    final.extend(words)
    phrase.extend(phrases)#print(phrase)

'''Compute unique words and their corresponding frequencies'''
keys, values = np.unique(final, return_counts=True)
values=values.tolist()
keys=keys.tolist()

keys_phrase, values_phrase = np.unique(phrase, return_counts=True)
values_phrase=values_phrase.tolist()
keys_phrase=keys_phrase.tolist()

res = {keys[i]: values[i] for i in range(len(keys))}
for key,value in res.items():
	if args.flag==" ":
		if key==args.word:
			print("The word '"+ args.word + "' occurs " + str(value)  + " times in " + args.filename)

res_phrase = {keys_phrase[i]: values_phrase[i] for i in range(len(keys_phrase))}
for key,value in res_phrase.items():
	if key==args.word + " " + args.flag:
		print("The phrase '"+ args.word + ' ' + args.flag + "' occurs " + str(value)  + " times in " + args.filename)

if args.word != res.keys():
	print("The input does not exist in Tweets.txt")
