import psycopg
conn = psycopg.connect('dbname= trendy user = gb760')
cur = conn.cursor()

query = '''
SELECT date_trunc('minute',time) as minute, count(DISTINCT word) as unique_words                           
FROM words
WHERE date_trunc('minute',time)  = date_trunc('minute', now()::timestamp) group by minute;
'''

def get_vocab(query):
  print(cur.execute(query).fetchall())
  # for i in cur:
  #   return i
  
  
get_vocab(query)
