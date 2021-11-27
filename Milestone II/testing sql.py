import psycopg

conn = psycopg.connect('dbname = trendy user = gb760')

cur = conn.cursor()

def get_results(query):
    cur.execute(query)
    for row in cur:
        print(row)
        #print row[0] to just extract the information inside the tuple instead of the whole object

q = '''
select * from words; 
'''
get_results(q)

print(cur.execute("select count(*) from words group by date_trunc('minute',time)").fetchall())
cur.close()