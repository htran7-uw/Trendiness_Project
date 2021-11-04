import requests
import os
import json
import pandas as pd
import datetime
import argparse
import time

#API Key = xWbz9qoquYQ2DdIXwJ6yNJq1G
#API Key Secret = 1SiQLpVlvTsnlKwHBqfnejuHLBGZUUUdoCFp3GpVytOMmYeLWU
#Bearer Token = AAAAAAAAAAAAAAAAAAAAAFBhUgEAAAAAhchmgzNuAQeIPOXeYqYx138AOu0%3De7gL0uj0UaOjETomEJJemvl2kdH7S8TNk6jz8SJPsN2rlpfTMt

'''Credentials'''
os.environ['BEARER_TOKEN'] = 'AAAAAAAAAAAAAAAAAAAAAFBhUgEAAAAAhchmgzNuAQeIPOXeYqYx138AOu0%3De7gL0uj0UaOjETomEJJemvl2kdH7S8TNk6jz8SJPsN2rlpfTMt'
bearer_token = os.environ.get("BEARER_TOKEN")
#print(bearer_token)

'''Optional --filename flag for json files'''
parser = argparse.ArgumentParser()
parser.add_argument('json',type=str, nargs = '?', help = 'Load a JSON file instead of the Twitter API')
args = parser.parse_args()
json_file = args.json

'''Authenticate myself as a user and read all tweets'''
'''Source code: 
https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/Sampled-Stream/sampled-stream.py
'''
path = os.getcwd()
#print(path)
if os.path.exists('Tweets.txt') == True:
    os.replace('Tweets.txt', 'Tweets.txt')
    print('We replaced the Tweets.txt file so you do not run out of disk space.')
else:
    open('Tweets.txt', 'w')
    print('We created a brand new file called Tweets.txt.')

txt_file = open('Tweets.txt','w')

def create_url():
    return "https://api.twitter.com/2/tweets/sample/stream?tweet.fields=created_at,lang"
#"https://api.twitter.com/2/tweets/sample/stream?tweet.fields=created_at,lang"
def bearer_oauth(r):
    '''
    Method required by bearer token authentication
    '''
    r.headers['Authorization'] = f"Bearer {bearer_token}"
    r.headers['User-Agent'] = "v2SampledStreamPython"
    return r

def connect_to_endpoint(url):
    response = requests.request("GET", url, auth = bearer_oauth, stream = True)
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

    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            print(json.dumps(json_response, indent=4, sort_keys=True))
            if json_response['data']['lang'] == 'en':
                timestamp = json_response['data']['created_at']
                timestamp = datetime.datetime.strptime(timestamp,'%Y-%m-%dT%H:%M:%S.%f%z')
                timestamp = datetime.datetime.strftime(timestamp, '%Y-%m-%d-%H-%M-%S')
                text = json_response['data']['text']
                each_tweet = [timestamp,',', text, '\n']
                txt_file.writelines(each_tweet)
            else:
                pass


def extract_json_file(file):
    f = open(file,'r')
    data = json.loads(f.read())
    json_response = json.loads(data)
    print(json.dumps(json_response, indent=4, sort_keys=True))
    if json_response['data']['lang'] == 'en':
        timestamp = json_response['data']['created_at']
        timestamp = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f%z')
        timestamp = datetime.datetime.strftime(timestamp, '%Y-%m-%d-%H-%M-%S')
        text = json_response['data']['text']
        each_tweet = [timestamp, ',', text, '\n']
        txt_file.writelines(each_tweet)
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
                print(f"Somebody paused the script!",'\n',"Re-run the script to continue. However, you will be overwriting your file if you do." ,'\n'
                      , "If you do not want to lose that file, store it somewhere else and then re-run the script.")
                break

if __name__ == "__main__":
    main()


