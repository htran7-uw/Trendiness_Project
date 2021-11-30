import json
import time
import datetime
import psycopg2
from tweet_log import logger
from kafka import KafkaConsumer
from kafka_conf import KAFKA_TOPIC, KAFKA_HOSTS

# after finish debug, change DEBUG to False
DEBUG = False 

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_HOSTS,
    enable_auto_commit=True,
    group_id='tweet-group-db',  # any name is OK
    value_deserializer=lambda x: x.decode('utf-8'))


connection = psycopg2.connect("dbname=trendy user=gb760 password=gb760")
cursor = connection.cursor()


def save_to_db(ts, text):
    #save to database
    timestamp_str = datetime.datetime.strftime(datetime.datetime.fromtimestamp(ts), '%Y-%m-%d-%H-%M-%S')
    # save timestamp_str and text to database
    query = '''INSERT INTO base VALUES (%s, %s, %s)'''
    cursor.execute(query, (ts, timestamp_str, text))
    connection.commit()


def process_data(rev_dict):
    ts = rev_dict['timestamp']
    text = rev_dict['text']
    timestamp_str = datetime.datetime.strftime(datetime.datetime.fromtimestamp(ts), '%Y-%m-%d-%H-%M-%S')
    if DEBUG:
        logger.debug('-- consumer receive success: ', timestamp_str, len(text), text[:200])
    save_to_db(ts, text)


def run():
    for m in consumer:
        rev_data = m.value
        try:
            rev_obj = json.loads(rev_data)
        except:
            logger.error('-- consumer receive bad: ', type(rev_data), rev_data[:200])
            continue
        process_data(rev_obj)

if __name__ =="__main__":
    run()

