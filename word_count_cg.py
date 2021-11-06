#!FULL_PATH_TO_PYTHON_INTERPRTER -m spacy download en
import re
import pandas as pd
import numpy as np 
import argparse  
import spacy

parser = argparse.ArgumentParser()
parser.add_argument('filename',type=str)
parser.add_argument('word',type=str,help='Display frequency of the user input')
parser.add_argument("flag", nargs="?", default=" ")
args = parser.parse_args()

final=[]

filename = args.filename
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
regex = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|
        mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br
        |bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo
        |jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""

def get_file(filename):
    with open(filename) as file:
        lines = file.readlines()
        tweets = pd.DataFrame(lines)
    return tweets

def clean_text(text):
    if type(text) != str:
        text = text.decode("utf-8")
    doc = re.sub(regex, '', text, flags=re.MULTILINE)  # remove URLs
    sentences = []
    for sentence in doc.split("\n"):
        if len(sentence) == 0:
            continue
        sentences.append(sentence)
    doc = nlp("\n".join(sentences))
    doc = " ".join([token.lemma_.lower().strip() for token in doc
                    if (not token.is_stop)
                    and (not token.like_url)
                    and (not token.lemma_ == "-PRON-")
                    and (not len(token) < 4)])
    return doc

def parse_tweets(tweets):
    tweets_empty = []
    for i, words in enumerate(tweets[0]):
        if words == '':
            tweets_empty.append(i)
    '''Check for empty lists'''
    try:
        tweets.drop([tweets_empty], axis=0, inplace=True)
    except KeyError:
        pass
    tweets.dropna(inplace=True)

    '''Break down the tweet and parse words only'''
    for i, words in enumerate(tweets[0]):
        new_words = clean_text(words)
        new_words = re.sub(r'[\d{4}\-\d{2}\-\d{2}\-\d{2}\-\d{2}\-\d{2},]', '', new_words)
        new_words = re.sub(r'@[a-z0-9\_]+', '', new_words)
        new_words = re.sub(r'\brt\b', '', new_words)
        final_list = re.findall(r"[^rt](?!'.*')\b[\w']+\b", new_words)
        #print(final_list)
        for i, word in enumerate(final_list):
            final_list[i] = str(word.strip())
        final.extend(final_list)

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
		
def main():
    twitter_df = get_file(filename)
    parse_tweets(twitter_df)
    print('Done!')

if __name__ == '__main__':
    main()

