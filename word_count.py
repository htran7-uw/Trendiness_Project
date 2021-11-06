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
	pass
tweets.dropna(inplace = True)

'''Break down the tweet and parse words only'''
for i, words in enumerate(tweets[0]):
	words = words.strip().lower()
	new_words = re.sub(r'[\d{4}\-\d{2}\-\d{2}\-\d{2}\-\d{2}\-\d{2},]','',words)
	new_words = re.sub(r'https://t.co/\w+', '', new_words)
	new_words = re.sub(r'@[a-z0-9\_]+','',new_words)
	final_list = re.findall(r"[^rt](?!'.*')\b[\w']+\b", new_words)
	for i, word in enumerate(final_list):
		final_list[i] = str(word.strip())
	final.extend(final_list)

phrase=[final[i]+ " " + final[i+1] for i in range(len(final)-1)]
#print(phrase)

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
