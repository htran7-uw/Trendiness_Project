import psycopg
from datetime import datetime
import argparse

conn = psycopg.connect('dbname= trendy user = gb760')
cur = conn.cursor()

parser = argparse.ArgumentParser()
parser.add_argument('word', type=str, help='Display frequency of the user input')
parser.add_argument("flag", nargs="?", default=" ")
args = parser.parse_args()


def get_unique_words():  # get the unique vocab size from the word database
    query = '''
    SELECT date_trunc('minute',time) as minute, count(DISTINCT word) as unique_words                           
    FROM words
    WHERE date_trunc('minute',time)  = date_trunc('minute', now()::timestamp) group by minute;
    '''
    while True:
        try:
            unique_word_count = cur.execute(query).fetchone()[1]
            assert isinstance(unique_word_count, int)
            return unique_word_count
        except TypeError as err:
            print(
                f"An error was returned, which means you either don't have any words in the current minute or the server script is not running")
            print(f"This is the error: {err}")
            break


# V = get_unique_words()

def get_unique_phrases():  # get the unique vocab size from the phrase database
    query = '''
    SELECT date_trunc('minute',time) as minute, count(DISTINCT phrase) as unique_phrases                         
    FROM phrases
    WHERE date_trunc('minute',time)  = date_trunc('minute', now()::timestamp) group by minute;
    '''
    while True:
        try:
            unique_phrase_count = cur.execute(query).fetchone()[1]
            assert isinstance(unique_phrase_count, int)
            return unique_phrase_count
        except TypeError as err:
            print(
                f"An error was returned, which means you either don't have any words in the current minute or the server script is not running")
            print(f"This is the error: {err}")
            break


def get_wc():  # get the word count of the user's input regardless of word or phrase
    min_var = "date_trunc('minute',time)"
    word = str("'" + args.word + "'")
    query = f"Select {min_var} as minute, count(*) from words where word = {word} and {min_var} = date_trunc('minute',now()::timestamp) group by minute;"
    while True:
        try:
            wc = cur.execute(query).fetchone()[1]  # get the count not the time
            return wc
        except TypeError as err:
            print(
                f"An error was returned, which means you either don't have any words in the current minute or the server script is not running")
            print(f"This is the error: {err}")
            break


def get_all_words():  # get all words at the current minute
    query = '''
        SELECT date_trunc('minute',time) as minute, count(*) as unique_words                           
        FROM words
        WHERE date_trunc('minute',time)  = date_trunc('minute', now()::timestamp) group by minute;
        '''
    while True:
        try:
            wc_all = cur.execute(query).fetchone()[1]
            assert isinstance(wc_all, int)
            return wc_all
        except TypeError as err:
            print(
                f"An error was returned, which means you either don't have any words in the current minute or the server script is not running")
            print(f"This is the error: {err}")
            break


def get_all_phrases():  # get all phrases at the current minute
    query = '''
        SELECT date_trunc('minute',time) as minute, count(*) as unique_words                           
        FROM phrases
        WHERE date_trunc('minute',time)  = date_trunc('minute', now()::timestamp) group by minute;
        '''
    while True:
        try:
            pc_all = cur.execute(query).fetchone()[1]
            assert isinstance(pc_all, int)
            return pc_all
        except TypeError as err:
            print(
                f"An error was returned, which means you either don't have any words in the current minute or the server script is not running")
            print(f"This is the error: {err}")
            break


word_count = 1 + get_wc()
V = get_unique_words()
total_phrases = V + get_all_phrases()
score = word_count / total_phrases
print(score)