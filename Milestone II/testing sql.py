import psycopg
import time
import datetime
import argparse
conn = psycopg.connect('dbname = trendy user = gb760')

cur = conn.cursor()

parser = argparse.ArgumentParser()
parser.add_argument('word', type=str, help='Display frequency of the user input')
parser.add_argument("flag", nargs="?", default=" ")
args = parser.parse_args()

word_list = [args.word.strip(),args.flag.strip().lower()]
print(word_list)
phrase = str(args.word + " " + args.flag)
phrase_2 = ' '.join(word_list)
print(len(phrase), phrase)
print(len(phrase_2), phrase_2)

def get_results(query):
    cur.execute(query)
    for row in cur:
        print(row)
        #print row[0] to just extract the information inside the tuple instead of the whole object

q = '''
select * from words; 
'''
def get_results(query):
    while True:
        try:
            results = cur.execute(query).fetchone()[1] #the query needs to have the time and count of word/phrase column. Collect the 2nd item of the tuple
            assert isinstance(results, int)
            return results
        except TypeError as err:
            seconds = 2
            print("Let's wait", seconds, "seconds and try again")
            time.sleep(seconds)
            results = cur.execute(query).fetchone()[1]
            return results



initial_datetime = datetime.datetime.now()
one_minute = datetime.timedelta(minutes = 1)
final_datetime = initial_datetime - one_minute
prev_min = final_datetime.minute
prev_date = datetime.datetime.strftime(final_datetime, '%Y-%m-%d-%H-%M-%S')
prev_date = datetime.datetime.strptime(prev_date, '%Y-%m-%d-%H-%M-%S')
print(prev_date)

min_var = "date_trunc('minute',time)"
word = 'covid'
q1 = f"Select {min_var} as minute, count(*) from words where word = '{word}' and {min_var} = date_trunc('minute', now()::timestamp) - interval '1 minute' group by minute;"
wc_previous = get_results(q1)
print(wc_previous)

#print(cur.execute("select count(*) from words group by date_trunc('minute',time)").fetchall())
cur.close()