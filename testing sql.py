import psycopg

conn = psycopg.connect('dbname = trendy user = gb760')

cur = conn.cursor()

def get_results(query):
    cur.execute(query)
    for row in cur:
        print(row)
        #print row[0] to just extract the information inside the tuple instead of the whole object

q = '''
select count(*) from words
where word = 'material'
group by time; 
'''
get_results(q)

cur.close()