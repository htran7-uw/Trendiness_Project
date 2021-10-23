import re
import pandas as pd
import numpy as np

with open('Tweets.txt') as file:
	lines = file.readlines()

#print(type(lines))

tweets = pd.DataFrame(lines)
#print(tweets.shape)
#print(tweets[0][1])
tweets_empty = []
for i, words in enumerate(tweets[0]):
	if words == '':
		tweets_empty.append(i)
try:
	tweets.drop([tweets_empty],axis = 0, inplace=True)
except KeyError:
	pass
tweets.dropna(inplace = True)

final_list = []

for i, words in enumerate(tweets[0]):
	words = words.strip().lower()
	#print(words)
	new_words = re.sub(r'[\d{4}\-\d{2}\-\d{2}\-\d{2}\-\d{2}\-\d{2},]','',words)
	new_words = re.sub(r'https://t.co/\w+', '', new_words)
	new_words = re.sub(r'@[a-z0-9\_]+','',new_words)
	#print(new_words)
	#Source code: https://stackoverflow.com/questions/27715581/how-do-i-handle-contractions-with-regex-word-boundaries-in-javascript
	word_list = re.findall(r"[^rt](?!'.*')\b[\w']+\b", new_words)
	final_list.append(word_list)

word_count = {}
for each_tweet in final_list:
	for word in each_tweet:
		word = word.strip()
		if word in word_count:
			word_count[word] += 1
		else:
			word_count[word] = 1
#print(word_count)
for count in word_count.items():
	print(count)


