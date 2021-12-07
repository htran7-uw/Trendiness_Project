import tweepy
import json
import time
import re
from kafka import KafkaProducer
from keys import *
from clean_text import clean_text
from kafka_conf import KAFKA_TOPIC, KAFKA_HOSTS

producer = KafkaProducer(bootstrap_servers=KAFKA_HOSTS, value_serializer=lambda x: json.dumps(x).encode('utf-8'))


def send_to_kafka(text):
    print('-- producer receive: ', len(text), text[:50])
    send_data = {
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

