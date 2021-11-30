import psycopg
import datetime
import argparse
import time

conn = psycopg.connect('dbname= trendy user = gb760')
cur = conn.cursor()

parser = argparse.ArgumentParser()
parser.add_argument('word', type=str, help='Display frequency of the user input')
parser.add_argument("flag", nargs="?", default=" ")
args = parser.parse_args()


def get_results(query):
    while True:
        try:
            results = cur.execute(query).fetchone()[1] #the query needs to have the time and count of word/phrase column. Collect the 2nd item of the tuple
            assert isinstance(results, int)
            return results
        except TypeError as err:
            for x in range(3):
                print(f"Attempt # {x}")
                seconds = 2
                print("Let's wait", seconds, "seconds and try again")
                time.sleep(seconds)
                if x == 2:
                    print("We can't find the word/phrase at the specified minute in sql so we're giving this query a result of 0")
                results = 0
            return results


def compute_ts(wc_curr, unique_curr, total_curr, wc_prev, unique_prev, total_prev):
    word_list = [args.word.lower().strip(), args.flag.lower().strip()]
    #print(word_list)
    w_or_p = ' '.join(word_list)
    curr_min = datetime.datetime.now().minute
    initial_datetime = datetime.datetime.now()
    one_minute = datetime.timedelta(minutes=1)
    final_datetime = initial_datetime - one_minute
    prev_min = final_datetime.minute
    prob_curr = (1 + wc_curr)/(unique_curr + total_curr)
    prob_prev = (1 + wc_prev)/(unique_prev + total_prev)
    score = prob_curr/prob_prev
    print(f'The probability of "{w_or_p}" at current minute {curr_min}: {prob_curr}')
    print(f'The probability of "{w_or_p}" at previous minute {prev_min}: {prob_prev}')
    print(f'The trendiness score of "{w_or_p}" is: {score}')
    return score

def main():
    '''check if it is a word or a phrase by the flag option'''
    word_list = [str(args.word.strip().lower()), str(args.flag.strip().lower())]
    #print(word_list)
    #print(args.word)
    #print(args.flag)
    #print(word_list)
    if args.flag == " ": #check if it's a word or phrase
        print('Searching in words table...')
        '''get word variables at the CURRENT minute'''
        #get # of times word was seen in current minute
        min_var = "date_trunc('minute',time)"
        word = args.word.lower().strip()
        print(f'Looking for number of times "{word}" was seen in the current minute')
        q1 = f"Select {min_var} as minute, count(*) from words where word = '{word}' and {min_var} = date_trunc('minute',now()::timestamp) group by minute;"
        wc_curr = get_results(q1)

        #get # of unique words in current minute
        q2 = f'''
            SELECT {min_var} as minute, count(DISTINCT word) as unique_words
            FROM words
            WHERE {min_var} = date_trunc('minute', now()::timestamp) group by minute;
            '''
        num_unique_words_current = get_results(q2)

        #get total # of words in current minute
        q3 = f'''
        SELECT {min_var} as minute, count(*) as unique_words
        FROM words
        WHERE {min_var}  = date_trunc('minute', now()::timestamp) group by minute;
        '''
        total_words_current = get_results(q3)

        '''get word variables at the previous minute'''
        #get # of times word was seen in previous minute
        print(f'Looking for # of times "{word}" was seen in the previous minute')
        min_var = "date_trunc('minute',time)"
        word = args.word.strip().lower()
        q1 = f"Select {min_var} as minute, count(*) from words where word = '{word}' and {min_var} = date_trunc('minute', now()::timestamp) - interval '1 minute' group by minute;"
        wc_prev = get_results(q1)
        #print(wc_previous)

        #get unique words in previous minute
        q2 = f'''   SELECT {min_var} as minute, count(DISTINCT word) as unique_words
                    FROM words
                    WHERE {min_var} = date_trunc('minute', now()::timestamp) - interval '1 minute' group by minute;
              '''
        num_unique_words_prev = get_results(q2)

        #get total number of words in previous minute
        q3 = f'''
                SELECT {min_var} as minute, count(*) as unique_words
                FROM words
                WHERE {min_var} = date_trunc('minute', now()::timestamp) - interval '1 minute' group by minute;
                '''
        total_words_prev = get_results(q3)

        #get the trendiness score
        compute_ts(wc_curr = wc_curr, unique_curr= num_unique_words_current, total_curr = total_words_current,
                   wc_prev= wc_prev, unique_prev = num_unique_words_prev, total_prev = total_words_prev)
    else:
        print('Searching in phrases table...')
        '''get phrase variables at the CURRENT minute'''
        min_var = "date_trunc('minute',time)"
        word_list = [str(args.word.strip().lower()),str(args.flag.strip().lower())]
        phrase = ' '.join(word_list)

        # get # of times phrase was seen in current minute
        print(f'Looking for number of times "{phrase}" was seen in the current minute')
        q1 = f"Select {min_var} as minute, count(*) from phrases where phrase = '{phrase}' and {min_var} = date_trunc('minute',now()::timestamp) group by minute;"
        pc_curr = get_results(q1)

        # get # of unique phrases in current minute
        q2 = f'''
            SELECT {min_var} as minute, count(DISTINCT phrase) as unique_phrases
            FROM phrases
            WHERE {min_var} = date_trunc('minute', now()::timestamp) group by minute;
            '''
        num_unique_phrases_current = get_results(q2)

        # get total # of words in current minute
        q3 = f'''
                SELECT {min_var} as minute, count(*) as total_phrases
                FROM phrases
                WHERE {min_var}  = date_trunc('minute', now()::timestamp) group by minute;
                '''
        total_phrases_current = get_results(q3)

        '''get phe variables at the previous minute'''
        # get # of times phrase was seen in previous minute
        print(f'Looking for number of times "{phrase}" was seen in the previous minute')
        min_var = "date_trunc('minute',time)"
        word = args.word.strip().lower()
        q1 = f"Select {min_var} as minute, count(*) from phrases where phrase = '{phrase}' and {min_var} = date_trunc('minute', now()::timestamp) - interval '1 minute' group by minute;"
        pc_prev = get_results(q1)
        # print(wc_previous)

        # get unique phrases in previous minute
        q2 = f'''   
                SELECT {min_var} as minute, count(DISTINCT phrase) as unique_phrases
                FROM phrases
                WHERE {min_var} = date_trunc('minute', now()::timestamp) - interval '1 minute' group by minute;
              '''
        num_unique_phrases_prev = get_results(q2)

        # get total number of phrases in previous minute
        q3 = f'''
            SELECT {min_var} as minute, count(*) as total_phrases
            FROM phrases
            WHERE {min_var} = date_trunc('minute', now()::timestamp) - interval '1 minute' group by minute;
              '''
        total_phrases_prev = get_results(q3)

        # get the trendiness score
        compute_ts(wc_curr=pc_curr, unique_curr=num_unique_phrases_current, total_curr=total_phrases_current,
                           wc_prev=pc_prev, unique_prev=num_unique_phrases_prev, total_prev=total_phrases_prev)
if __name__ == '__main__':
    main()