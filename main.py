from preprocess import CustomTokenizer
from statistics import TfidfRanker
import CustomGUI as gui
import pickle

'''
This script opens the locally downloaded pages from the crawler, preprocess them, builds inverted index and
runs page rank, computes docs lengths, it then stores inverted index, page rank and docs length with pickle
'''
PAGE_RANK_MAX_ITER = 100
N_PAGES = 10000

USE_PAGE_RANK = True


def load_files():
    """Loading all the necessary files to run the queries and return ranked urls"""

    global url_from_code, code_from_url, inverted_index, docs_length, page_ranks

    with open('url_from_code_dict.pickle', 'rb') as handle:
        url_from_code = pickle.load(handle)
    with open('code_from_url_dict.pickle', 'rb') as handle:
        code_from_url = pickle.load(handle)
    with open('inverted_index_dict.pickle', 'rb') as handle:
        inverted_index = pickle.load(handle)
    with open('doc_lengths_dict.pickle', 'rb') as handle:
        docs_length = pickle.load(handle)
    with open('page_ranks_dict.pickle', 'rb') as handle:
        page_ranks = pickle.load(handle)


def new_query():
    query = gui.ask_query()
    if query is None:
        exit()
    print(query)
    print(tokenizer.tokenize(query))
    choice = gui.display_query_results(tf_idf_ranker.retrieve_most_relevant(tokenizer.tokenize(query), True)[:10],
                                       url_from_code)
    print(choice)


load_files()
tokenizer = CustomTokenizer(N_PAGES)
tf_idf_ranker = TfidfRanker(inverted_index, N_PAGES, page_ranks, docs_length)


while 1:
    new_query()
