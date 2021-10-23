import requests
import os
import json
import pandas as pd
import datetime
#API Key = xWbz9qoquYQ2DdIXwJ6yNJq1G
#API Key Secret = 1SiQLpVlvTsnlKwHBqfnejuHLBGZUUUdoCFp3GpVytOMmYeLWU
#Bearer Token = AAAAAAAAAAAAAAAAAAAAAFBhUgEAAAAAhchmgzNuAQeIPOXeYqYx138AOu0%3De7gL0uj0UaOjETomEJJemvl2kdH7S8TNk6jz8SJPsN2rlpfTMt

os.environ['BEARER_TOKEN'] = 'AAAAAAAAAAAAAAAAAAAAAFBhUgEAAAAAhchmgzNuAQeIPOXeYqYx138AOu0%3De7gL0uj0UaOjETomEJJemvl2kdH7S8TNk6jz8SJPsN2rlpfTMt'
bearer_token = os.environ.get("BEARER_TOKEN")
print(bearer_token)


'''Part A: Authenticate myself as a user and read all tweets'''
'''Source code: https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/Sampled-Stream/sampled-stream.py'''
path = os.getcwd()
print(path)
if os.path.exists('Tweets.txt') == True:
    os.replace('Tweets.txt', 'Tweets.txt')
    print('We replaced the file, but it has the same name.')
else:
    open('Tweets.txt', 'w')
    print('We created a brand new file called Tweets.txt.')

txt_file = open('Tweets.txt','w')

def create_url():
    return "https://api.twitter.com/2/tweets/sample/stream?tweet.fields=created_at,lang"

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
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
def main():
    url = create_url()
    timeout = 0
    while True:
        try:
            connect_to_endpoint(url)
            timeout += 1
        except KeyboardInterrupt as err:
            print(f"Somebody paused the script!")
            break

if __name__ == "__main__":
    main()


