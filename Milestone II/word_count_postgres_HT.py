import argparse
import psycopg
from datetime import datetime

conn = psycopg.connect('dbname= trendy user = gb760')
cur = conn.cursor()

parser = argparse.ArgumentParser()
parser.add_argument('word',type=str,help='Display frequency of the user input')
parser.add_argument("flag", nargs="?", default=" ")
args = parser.parse_args()

def main():
    min_var = "date_trunc('minute',time)"
    word = str("'" + args.word + "'")
    current_minute = datetime.now().minute
    query = f"Select {min_var} as minute, count(*) from words where word = {word} and {min_var} = date_trunc('minute',now()::timestamp) group by minute;"
    while True:
        try:
            result = cur.execute(query).fetchone()[1] #get the count not the time
            print(f"The word or phrase {word} appears for {result} times at minute {current_minute}")
            break
        except TypeError as err:
            print(f"An error was returned, which means you either don't have any words in the current minute or the server script is not running")
            print(f"This is the error: {err}")
            break

if __name__ == '__main__':
    main()