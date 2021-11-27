import argparse
import psycopg2

conn = psycopg2.connect('dbname= trendy user = gb760')
cur = conn.cursor()

parser = argparse.ArgumentParser()
parser.add_argument('word',type=str,help='Display frequency of the user input')
parser.add_argument("flag", nargs="?", default=" ")
args = parser.parse_args()

#select date_trunc('minute', time), count(*) from words where word ='suck' and date_trunc('minute', time) = date_trunc('minute',current_timestamp) group by date_trunc('minute',time);
cur.execute("Select count(*) from words where word = 'word' and date_trunc('minute', time) = date_trunc('minute', current_timestamp);")

results = cur.fetchall()
for r in results:
	print(r)
