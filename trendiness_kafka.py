import json
import datetime
import time
import psycopg2
import argparse
from tweet_log import logger
from kafka import KafkaConsumer
from kafka_conf import KAFKA_TOPIC, KAFKA_HOSTS
from trend_score import trend_score
from word_count import word_reservioir, hash_word_reservioir, get_hash_word_count, get_vocabulary_size, get_total_words,get_word_count



connection = psycopg2.connect("dbname=trendy user=gb760")
cursor = connection.cursor()



consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_HOSTS,
    enable_auto_commit=True,
    group_id='tweet-group-trendiness',  # any name is OK
    value_deserializer=lambda x: x.decode('utf-8'))


online_data = []
START_TIME = 0
LAST_RESULT_TIME = 0
LAST_INFO_TIME = 0
TREND_DURATION = 60

def process_data(rev_dict, word, is_hash, is_nlp):
    ts = rev_dict['timestamp']
    text = rev_dict['text']
    timestamp_str = datetime.datetime.strftime(datetime.datetime.fromtimestamp(ts), '%Y-%m-%d-%H-%M-%S')
    # analysis the words
    analyze_dynamic_trendiness_score(ts, text, word, is_hash, is_nlp)


def analyze_dynamic_trendiness_score(ts, new_text, word, is_hash, is_nlp):
    global START_TIME
    global LAST_RESULT_TIME
    global LAST_INFO_TIME 
    global TREND_DURATION
    global online_data

    if not new_text:
        # in some case not data
        return

    online_data.append([ts, new_text])

    t = int(time.time())
    if t - START_TIME <= TREND_DURATION * 2:
        # we do not have enough data
        if t - LAST_INFO_TIME >= 10:
            LAST_INFO_TIME = t
            print("We only have %d seconds data in kafka. Still collecting data" % (t - START_TIME))
        return 

    if t - LAST_RESULT_TIME >= 10:
        LAST_RESULT_TIME = t

        # clear the list
        new_list = [r for r in online_data if r[0] >= t - TREND_DURATION * 2]
        online_data = new_list
        if not online_data:
            return
     
        my_trendiness_score(
            [{'t': r[0], 'text': r[1]} for r in online_data if r[0] < t],
            # word is the given search word
            # online_data[-1] is the latest in the list
            word, online_data[-1][0],
            is_hash, is_nlp
        )


def my_trendiness_score(text_list, word, end_ts, is_hash, is_nlp):
    global TREND_DURATION
    result = trend_score(text_list, word, end_ts, TREND_DURATION, is_hash, is_nlp)
    
    print("--- during %s to %s, word: %s trendiness score is %s ---" % ( 
        datetime.datetime.strftime(datetime.datetime.fromtimestamp(end_ts - TREND_DURATION), '%Y-%m-%d-%H-%M-%S'),
        datetime.datetime.strftime(datetime.datetime.fromtimestamp(end_ts), '%Y-%m-%d-%H-%M-%S'),
        word, result['score']
    ))
    print("    current minute info: word count: %d, vocabulary size %d, total %d" % (
        result['current_word_count'], result['current_vocabulary_size'], result['current_total_count'], 
    ))
    print("    prior minute info: word count: %d, vocabulary size %d, total %d" % (
        result['prior_word_count'], result['prior_vocabulary_size'], result['prior_total_count'], 
    ))
    return 


def run(word, is_hash, is_nlp):
    global START_TIME
    START_TIME = int(time.time())

    for m in consumer:
        rev_data = m.value
        try:
            rev_obj = json.loads(rev_data)
        except: 
            logger.error('-- consumer receive bad: ', type(rev_data), rev_data[:200])
            continue
        process_data(rev_obj, word, is_hash, is_nlp)



if __name__ =="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--word')
    parser.add_argument('--use_hash', help='1 or 0, by default is 0')
    parser.add_argument('--use_nlp', help='1 or 0, by default is 0, which only divide text by space')
    args = parser.parse_args()

    is_hash = int(args.use_hash) if args.use_hash else 0
    is_nlp = int(args.use_nlp) if args.use_nlp else 0
    run(args.words, is_hash, is_nlp)
