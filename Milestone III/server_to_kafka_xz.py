import tweepy
import json
import spacy
import re
from time import sleep
from json import dumps
from kafka import KafkaProducer
from keys import *


def send_data_to_kafka(text):
    print('-- producer receive: ', len(text), text[:50])
    send_data = {
        # we record the time at producer, because, after kafka, we may have seconds - minutes delay
        # we send 'int' not 'str' to consumer, because int is smaller
        'timestamp': int(time.time()),
        'text': text,
    }
    producer.send(KAFKA_TOPIC, value=send_data)
    return True
	
	
	
class MaxStream(tweepy.streaming.Stream):

    def on_data(self,raw_data):
        #Overwrite the default on_data
        self.process_data(raw_data)
        return True
		
    def process_data(self,raw_data):
        data = json.loads(raw_data)
        text_data = data.get('text', '')
        #print for debug
        print(text_data)
        if not text_data:
            return
        else:
    	    new_text = clean_text(text_data)
    	    send_to_kafka(new_text)
    
	
    def start(self):
        self.sample(languages=['en'])
           


#start the stream

if __name__ =="__main__":
	stream = MaxStream(consumer_key, consumer_secret, access_token, access_token_secret)
	stream.start()

