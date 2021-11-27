import psycopg
import datetime as d

conn = psycopg.connect('dbname= trendy user = gb760')
cur = conn.cursor()

query = '''
SELECT date_trunc('minute',time) as minute, count(DISTINCT word) as unique_words                           
FROM words
WHERE date_trunc('minute',time)  = date_trunc('minute', now()::timestamp) group by minute;
'''


def get_vocab(q):
    current_minute = d.datetime.now().minute
    while True:
        try:
            result = cur.execute(q).fetchone()[1] # get the count, not the time
            print(f'Number of unique words at minute {current_minute}: {result}')
            break
        except TypeError as err:
            print(f"An error was returned, which means you either don't have any words in the current minute or the server script is not running")
            print(f"This is the error: {err}")
            break

get_vocab(query)
