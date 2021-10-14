# NOT COMPLETE
import requests
import os
import json
import pandas as pd
import datetime
import argparse as ap 

# open Tweets.txt file 
with open('Tweets.txt', 'r') as f:
    lines = f.readlines()

df = pd.DataFrame(columns = ['all', 'date', 'text'])
df['all'] = lines
df['date'], df['text'] = df['all'].str.split(',',1).str

def main(phrase):
    count = 0
    for i in df['text']:
       words = i.split(' ')
       for word in words:
           if phrase == word:
               count = count + 1
    print('This phrase occurs ' + str(count) + ' times.')

