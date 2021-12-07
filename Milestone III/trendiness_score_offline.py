import datetime
import time
import psycopg2
import argparse
from trend_score import trend_score


connection = psycopg2.connect("dbname=trendy user=gb760")
cursor = connection.cursor()


def my_trendiness_score(word, start_ts, end_ts, is_hash=0, is_nlp=0):
    query = '''SELECT * from base where t >= %s and t < %s'''
    cursor.execute(query, (start_ts, end_ts))
    result = cursor.fetchall()

    # get all text data with time
    data_list = [{
        't': r[0],
        'text': r[2]
    } for r in result]

    # get score
    result = trend_score(data_list, word, end_ts, 60, is_hash, is_nlp) 

    print("--- during %s to %s, word: %s trendiness score is %s ---" % ( 
        datetime.datetime.strftime(datetime.datetime.fromtimestamp(end_ts - 60), '%Y-%m-%d-%H-%M-%S'),
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


if __name__ =="__main__":
    # we can run this function by calling word_count(xxx) in code
    # or, we can directly call this function by command-line
    parser = argparse.ArgumentParser()
    parser.add_argument('--word')
    parser.add_argument('--use_hash', help='1 or 0, by default is 0')
    parser.add_argument('--use_nlp', help='1 or 0, by default is 0, which only divide text by space')
    parser.add_argument('--time', help='Given time in yyyy-mm-dd-HH-MM-SS')
    args = parser.parse_args()

    if args.time:
        t = datetime.datetime(*[int(r) for r in args.time.split('-')])
        end = int(time.mktime(t.timetuple()))
        start = end - 60
    else:
        end = int(time.time())
        start = end - 60

    is_hash = int(args.use_hash) if args.use_hash else 0
    is_nlp = int(args.use_nlp) if args.use_nlp else 0

    my_trendiness_score(args.word.lower(), start-60, end, is_hash, is_nlp)

