import argparse
import psycopg

conn = psycopg.connect('dbname= trendy user = gb760')
cur = conn.cursor()

parser = argparse.ArgumentParser()
parser.add_argument('word',type=str,help='Display frequency of the user input')
parser.add_argument("flag", nargs="?", default=" ")
args = parser.parse_args()

min_var = "date_trunc('minute',time)"
word = str("'" + args.word + "'")
print(word)
print(cur.execute(f"Select {min_var} as minute, count(*) from words where word = {word} and "
                  f"{min_var} = date_trunc('minute',now()::timestamp) group by minute;").fetchall())
# results = cur.fetchall()
# for r in results:
# 	print(r)
