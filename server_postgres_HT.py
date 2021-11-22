import requests
import os
import json
import pandas as pd
import datetime
import argparse
import time
import psycopg
import re
import nlp
import spacy
import pytz
import subprocess

# API Key = xWbz9qoquYQ2DdIXwJ6yNJq1G
# API Key Secret = 1SiQLpVlvTsnlKwHBqfnejuHLBGZUUUdoCFp3GpVytOMmYeLWU
# Bearer Token = AAAAAAAAAAAAAAAAAAAAAFBhUgEAAAAAhchmgzNuAQeIPOXeYqYx138AOu0%3De7gL0uj0UaOjETomEJJemvl2kdH7S8TNk6jz8SJPsN2rlpfTMt

'''Credentials'''
os.environ[
    'BEARER_TOKEN'] = 'AAAAAAAAAAAAAAAAAAAAAFBhUgEAAAAAhchmgzNuAQeIPOXeYqYx138AOu0%3De7gL0uj0UaOjETomEJJemvl2kdH7S8TNk6jz8SJPsN2rlpfTMt'
bearer_token = os.environ.get("BEARER_TOKEN")
# print(bearer_token)

'''Optional --filename flag for json files'''
parser = argparse.ArgumentParser()
parser.add_argument('json', type=str, nargs='?', help='Load a JSON file instead of the Twitter API')
args = parser.parse_args()
json_file = args.json

'''Authenticate myself as a user and read all tweets'''
'''Source code: 
https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/Sampled-Stream/sampled-stream.py
'''

def create_url():
    return "https://api.twitter.com/2/tweets/sample/stream?tweet.fields=created_at,lang"


# "https://api.twitter.com/2/tweets/sample/stream?tweet.fields=created_at,lang"
def bearer_oauth(r):
    '''
    Method required by bearer token authentication
    '''
    r.headers['Authorization'] = f"Bearer {bearer_token}"
    r.headers['User-Agent'] = "v2SampledStreamPython"
    return r

connection = psycopg.connect("dbname=trendy user=gb760")
cursor = connection.cursor()

'''Clean the tweets coming in'''
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
regex = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|
        mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br
        |bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo
        |jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""
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

def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth, stream=True)
    print(response.status_code)
    if response.status_code != 200:
        for x in range(0, 6):
            print('Attempt #' + str(x))
            status = response.status_code
            if status != 200:
                print('The error code is still ' + str(status) + '.')
                seconds = 2
                print("Let's wait", seconds, "seconds and try again")
                time.sleep(seconds)
            else:
                print('Wait it actually worked!')
                break
        print('Looks like we still get an error code of', str(status), "You might have the wrong URL inserted.")
    print('Adding tweets... terminate the script to stop the program.')
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            #rint(json.dumps(json_response, indent=4, sort_keys=True))
            if json_response['data']['lang'] == 'en':
                timestamp = json_response['data']['created_at']
                timestamp = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f%z')
                central = pytz.timezone('US/Central')
                timestamp_central = timestamp.astimezone(central)
                timestamp_final = datetime.datetime.strftime(timestamp_central, '%Y-%m-%d-%H-%M-%S')
                text = clean_text(json_response['data']['text'])
                query = '''INSERT INTO base VALUES (%s, %s)'''
                cursor.execute(query, (timestamp_final, text))
                connection.commit()

                words = text.strip().lower()
                new_words = re.sub(r'[\d{4}\-\d{2}\-\d{2}\-\d{2}\-\d{2}\-\d{2},]', '', words)
                new_words = re.sub(r'https://t.co/\w+', '', new_words)
                new_words = re.sub(r'@[a-z0-9\_]+', '', new_words)
                final_list = re.findall(r"[^rt](?!'.*')\b[\w']+\b", new_words)
                final_list = [final_list[i].strip() for i in range(0,len(final_list))]
                for i in final_list:
                    '''Insert words into word table'''
                    word_query = '''INSERT INTO words VALUES (%s, %s)'''
                    cursor.execute(word_query, (timestamp_central, i))
                    connection.commit()

                    '''Insert phrases into phrase table'''
                phrase = [final_list[i]+ " " + final_list[i+1] for i in range(len(final_list)-1)]
                for x in phrase:
                    phrase_query = '''INSERT INTO phrases VALUES (%s, %s)'''
                    cursor.execute(phrase_query, (timestamp_central, x))
                    connection.commit()
            else:
                pass


def extract_json_file(file):
    f = open(file, 'r')
    data = json.loads(f.read())
    json_response = json.loads(data)
    print(json.dumps(json_response, indent=4, sort_keys=True))
    if json_response['data']['lang'] == 'en':
        timestamp = json_response['data']['created_at']
        timestamp = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f%z')
        central = pytz.timezone('US/Central')
        timestamp_central = timestamp.astimezone(central)
        timestamp_final = datetime.datetime.strftime(timestamp_central, '%Y-%m-%d-%H-%M-%S')
        text = json_response['data']['text']
        each_tweet = [timestamp, ',', text]
        query = '''INSERT INTO base VALUES (%s, %s)'''
        cursor.execute(query, (timestamp_final, text))
        connection.commit()
    else:
        pass


def main():
    if json_file:
        print("Looks like we're going to be working with a JSON file")
        extract_json_file(json_file)
    else:
        url = create_url()
        timeout = 0
        while True:
            try:
                connect_to_endpoint(url)
                timeout += 1
            except KeyboardInterrupt:
                print(f"Somebody paused the script!", '\n',
                      "Re-run the script to continue. However, you will be overwriting your file if you do.", '\n'
                      , "If you do not want to lose that file, store it somewhere else and then re-run the script.")
                break


if __name__ == "__main__":
    main()

