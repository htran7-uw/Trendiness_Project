import math
import time
import datetime
from word_count import word_reservioir, hash_word_reservioir, get_hash_word_count, get_vocabulary_size, get_total_words, get_word_count


def prob(target_word_count, unique_word_count, total_word_count):
    b = unique_word_count + total_word_count
    if not b:
        return 0
    return (1 + target_word_count) / b


def score(p_current, p_prior):
    if p_current > 0 and p_prior > 0: 
        return math.log10(p_current) - math.log10(p_prior)
    else:
        print("prob is 0, cannot use Log10")
        return 0


def trend_score(data_list, word, last_t, dur=60, is_hash=0, is_nlp=0):
    '''
    Args:
        data_list: a list of data contains {'t', 'time', 'text'}
            t - timestamp, 
            time - time string (which is not used for calculate
            text - text value
        word: str, the given word
        last_t: int, timestamp
        dur: we count [last_t-dur, last_t] as current time
             if dur=60, then, current 1 min
        is_hash: we use "hash(word)" to count freq
        is_nlp: 1 use nlp to split word. 0 is use space. by default is 0

    Return:
        trendiness_score:
            Log10(Prob(word | current minute at t)) - Log10(Prob(word | minute prior to t))

                                        1 + "word" appear times in t
            Prob(word | t) = -------------------------------------------------
                              unique words in t + all words appear times in t
    '''
    cur_min = [last_t - dur, last_t]   # get current minute 'start, end'
    prior_min = [cur_min[0] - dur, cur_min[1] - dur]  # prior minute 'start, end'

    # get prob(word | current minute)
    cur_data = [r['text'] for r in data_list if cur_min[0] <= r['t'] < cur_min[1]]
    if is_hash:
        cur_words_reservioir = hash_word_reservioir(cur_data, is_nlp)
        cur_w_count = get_hash_word_count(cur_words_reservioir, word)
    else:
        cur_words_reservioir = word_reservioir(cur_data,is_nlp)
        cur_w_count = get_word_count(cur_words_reservioir, word)

    cur_v = get_vocabulary_size(cur_words_reservioir)
    cur_all = get_total_words(cur_words_reservioir)
    prob_cur = prob(cur_w_count, cur_v, cur_all)

    # get prob(word | prior minute)
    prior_data = [r['text'] for r in data_list if prior_min[0] <= r['t'] < prior_min[1]]
    if is_hash:
        prior_words_reservioir = hash_word_reservioir(prior_data, is_nlp)
        prior_w_count = get_hash_word_count(prior_words_reservioir, word)
    else:
        prior_words_reservioir = word_reservioir(prior_data,is_nlp)
        prior_w_count = get_word_count(prior_words_reservioir, word)
        
    prior_v = get_vocabulary_size(prior_words_reservioir)
    prior_all = get_total_words(prior_words_reservioir)
    prob_prior = prob(prior_w_count, prior_v, prior_all)

    # trendiness_score
    result = score(prob_cur, prob_prior)
    # do something before return. for example, print the result?

    return {
        'current_word_count': cur_w_count,
        'current_vocabulary_size': cur_v,
        'current_total_count': cur_all,
        'prior_word_count': prior_w_count,
        'prior_vocabulary_size': prior_v,
        'prior_total_count': prior_all,
        'score': result,
    }

