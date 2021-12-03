import re
import argparse
import spacy
from tweet_log import logger


nlp = spacy.load('en_core_web_sm')


# added ignore words in the analysis, since they are not meaningful.
words_ignore = [
    'a', 'the',
    'i', 'you', 'he', 'your', 'him', 'her', 'his', 'me', 'we', 'it',
    'am', 'is', 'are', 'were', 'was',
    'has', 'have', 'had',
    'one', 'two', 'three',
    'who', 'what', 'when', 'where', 'how',  
    'to', 'in', 'on', 'of', 'and', 'for', 
    'this', 'that', 'these', 'they', 
    '-', '_', '#', '@', '%', '*',
    'rt',  # these are most freq words but meanless
]



def word_reservioir(data_list, is_nlp=0):
    """
    Count the data_list into a vocabulary dict
    
    Args:
        data_list: ['tweet text1', 'tweet text2']
        is_nlp: 1 use nlp, 0 not. by default is 0

    Return:
        {
            k: c,
        }
        # k = word, c = count
        e.g, {'this': 1, 'is': 1, 'game': 2, ...}
    """
    all_words_count = dict()
    
    for text in data_list:
        # get words from one sentence
        # choose one of below two ways:
        if is_nlp:
            # way-1, this is split words by nlp
            doc = nlp(text)
            words = [r.text.strip().lower() for r in doc.noun_chunks]
        else:
            # way-2, this is split words by non-nlp
            words = text.split(' ')

        words = [r for r in words if r and r != 'rt']  # remove empty words
        words = [r for r in words if not r.startswith('@')]  # remove '@xyz'
        words = [r for r in words if not r.lower().startswith('rt ')]  # remove 'rt @...'

        # count words to a dict. {k: c}, k = word, c = count
        # e.g, word_counts = {'this': 1, 'is': 1, 'game': 2, ...}
        word_counts = {r: words.count(r) for r in words}
        # save the result to "all word count"
        for k, v in word_counts.items():
            all_words_count.setdefault(k, 0)  # set default to 0, if k not exist.
            all_words_count[k] = all_words_count[k] + v

    return all_words_count


def hash_word_reservioir(data_list, is_nlp=0):
    """
    Count the data_list into a hashed vocabulary dict
    
    Args:
        data_list: ['tweet text1', 'tweet text2']
        is_nlp: 1 use nlp, 0 not. by default is 0

    Return:
        {
            hash(k): c
        }
        # k = word, c = count
        e.g, {0x123456: 1, 0x24689: 1, 0x135778: 2, ...}
    """
    all_hash_words_count = dict()
    
    for text in data_list:
        # get words from one sentence
        # choose one of below two ways:
        if is_nlp:
            # way-1, this is split words by nlp
            doc = nlp(text)
            words = [r.text.strip().lower() for r in doc.noun_chunks]
        else:
            # way-2, this is split words by non-nlp
            words = text.split(' ')

        words = [r for r in words if r and r != 'rt']  # remove empty words
        words = [r for r in words if not r.startswith('@')]  # remove '@xyz'
        words = [r for r in words if not r.lower().startswith('rt ')]  # remove 'rt @...'

        # in this step, two words may have the same 'hash' value
        # to solve this problem, we need make hash-deeper.
        hash_words = [hash(r) for r in words]
        hash_word_counts = {r: hash_words.count(r) for r in hash_words}
        for k, v in hash_word_counts.items():
            all_hash_words_count.setdefault(k, 0)  # set default to 0, if k not exist.
            all_hash_words_count[k] = all_hash_words_count[k] + v

    return all_hash_words_count


def get_word_count(word_reservioir, word):
    """
    Count the number of word in data_list 
    """
    return word_reservioir.get(word, 0)


def get_hash_word_count(hash_word_reservioir, word):
    return hash_word_reservioir.get(hash(word), 0)


def get_vocabulary_size(word_or_hash_reservioir):
    # get vocabulary size is easy
    # just count how many keys in reservioir
    return len(word_or_hash_reservioir.keys())


def get_total_words(word_or_hash_reservioir):
    # get total words is easy
    # reservioir is {k: c}  # c is count of k
    # so, just add all "c" which is reservioir.values()
    return sum(word_or_hash_reservioir.values())
