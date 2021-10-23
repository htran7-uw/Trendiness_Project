import re
import pandas as pd
import numpy as np 

final=[]

with open('Tweets.txt') as file:
	lines = file.readlines()

print(type(lines))

tweets = pd.DataFrame(lines)
print(tweets.shape)
print(tweets[0][1])
tweets_empty = []
for i, words in enumerate(tweets[0]):
	if words == '':
		tweets_empty.append(i)
try:
	tweets.drop([tweets_empty],axis = 0, inplace=True)
except KeyError:
	pass
tweets.dropna(inplace = True)
for i, words in enumerate(tweets[0]):
	words = words.strip().lower()
	print(words)
	# word_list = re.split(r"[\b\W\b]+", words.strip().lower())
	# #word_list = word_list.drop()
	# print(word_list)
	#word_list = re.split(r'.', words.strip())
	new_words = re.sub(r'[\d{4}\-\d{2}\-\d{2}\-\d{2}\-\d{2}\-\d{2},]','',words)
	new_words = re.sub(r'https://t.co/\w+', '', new_words)
	new_words = re.sub(r'@[a-z0-9\_]+','',new_words)
	final_list = re.findall(r"[^rt](?!'.*')\b[\w']+\b", new_words)
	final.extend(final_list)
	

keys, values = np.unique(final, return_counts=True)
values=values.tolist()
keys=keys.tolist()

res = {keys[i]: values[i] for i in range(len(keys))}
print(res)
