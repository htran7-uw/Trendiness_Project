# NOT COMPLETE
import requests
import os
import json
import pandas as pd
import datetime
import argparse  


parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()
with open(args.filename) as file:
	lines=file.readlines()

df = pd.DataFrame(lines)
df['date'], df['text'] = df.iloc[0].str.split(',',1).str
print(df['date'])
print(df['text'])

def main(phrase):
    count = 0
    for i in df['text']:
       words = i.split(' ')
       for word in words:
           if phrase == word:
               count = count + 1
    print('This phrase occurs ' + str(count) + ' times.')
