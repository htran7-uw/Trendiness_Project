import psycopg
conn = psycopg.connect('dbname= trendy user = gb760')
cur = conn.cursor()

query = '''
SELECT count(DISTINCT word)
FROM words
WHERE time = date_trunc('minute', now()::timestamp);
'''

def get_vocab(query):
  cur.execute(query)
  for i in cur:
    return i
  
  
get_vocab(query)
