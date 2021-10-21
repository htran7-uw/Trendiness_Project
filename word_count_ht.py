import re
import pandas as pd

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
	print(words.strip())
	word_list = re.split(r"\s+", words.strip())
	print(word_list)

# for i in tweets[0]:
# 	print(i)
