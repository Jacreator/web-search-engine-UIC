from preprocess import CustomTokenizer
from statistics import TfidfRanker, add_page_rank_scores_and_reorder
import CustomGUI as gui
import pickle
import time
from pseudo_relevance_feedback import CustomPseudoRelevanceFeedback

'''
This script opens the locally downloaded pages from the crawler, preprocess them, builds inverted index and
runs page rank, computes docs lengths, it then stores inverted index, page rank and docs length with pickle
'''
PAGE_RANK_MAX_ITER = 100
N_PAGES = 10000
RESULTS_PER_PAGE = 10
MAX_RESULTS_TO_CONSIDER = 100

USE_PAGE_RANK = False
USE_PAGE_RANK_EARLY = False  # I decided not to let the user choose this mode
USE_PSEUDO_RELEVANCE_FEEDBACK = True


def load_files():
    """Loading all the necessary files to run the queries and return ranked urls"""

    global url_from_code, code_from_url, inverted_index, docs_length, page_ranks, docs_tokens

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
    with open('docs_tokens_dict.pickle', 'rb') as handle:
        docs_tokens = pickle.load(handle)


def new_query():
    query = gui.ask_query()
    if query is None:
        exit()
    print(query)
    query_tokens = tokenizer.tokenize(query)
    print(query_tokens)

    best_ranked = tf_idf_ranker.retrieve_most_relevant(query_tokens, USE_PAGE_RANK_EARLY)[:MAX_RESULTS_TO_CONSIDER]

    if USE_PSEUDO_RELEVANCE_FEEDBACK:
        handle_pseudo_relevance_query(query_tokens, best_ranked)
    else:
        handle_normal_query(query_tokens, best_ranked)

    # choice = gui.display_query_results(tf_idf_ranker.retrieve_most_relevant(query_tokens)
    #                                    [:RESULTS_PER_PAGE], url_from_code)
    # print(choice)


def handle_normal_query(query_tokens, best_ranked):
    # still have to apply page rank if user chose it
    if USE_PAGE_RANK:
        best_ranked = add_page_rank_scores_and_reorder(best_ranked, page_ranks)
    handle_show_query(best_ranked, query_tokens, RESULTS_PER_PAGE)
    # choice = gui.display_query_results(best_ranked[:RESULTS_PER_PAGE], url_from_code, query_tokens)


def handle_pseudo_relevance_query(query_tokens, best_ranked):
    # remember to apply page rank to expanded query
    pseudo_relevance_feedback = CustomPseudoRelevanceFeedback(inverted_index, best_ranked, docs_tokens)
    # context_words = pseudo_relevance_feedback.run_pseudo_relevance()
    pseudo_relevance_feedback.run_pseudo_relevance()
    query_expansion_tokens = pseudo_relevance_feedback.get_query_expansion_tokens(query_tokens)

    best_ranked_expanded = tf_idf_ranker.retrieve_most_relevant_expanded(query_tokens,
                                                                         query_expansion_tokens)[:MAX_RESULTS_TO_CONSIDER]
    handle_show_query_expanded(best_ranked_expanded, query_tokens, query_expansion_tokens, RESULTS_PER_PAGE)

    print(query_expansion_tokens)


def handle_show_query(best_ranked, query_tokens, n):
    choice = gui.display_query_results(best_ranked[:n], url_from_code, query_tokens)

    if choice == 'Show more results':
        handle_show_query(best_ranked, query_tokens, n + RESULTS_PER_PAGE)
    else:
        if choice is None:
            pass
        else:
            print(choice)


def handle_show_query_expanded(best_ranked, query_tokens, query_expansion_tokens, n):
    choice = gui.display_query_results_expanded(best_ranked[:n], url_from_code, query_tokens, query_expansion_tokens)

    if choice == 'Show more results':
        handle_show_query_expanded(best_ranked, query_tokens, query_expansion_tokens, n + RESULTS_PER_PAGE)
    else:
        if choice is None:
            pass
        else:
            print(choice)


start = time.time()

load_files()

end = time.time()
print(str(end - start) + ' seconds')
tokenizer = CustomTokenizer(N_PAGES)
tf_idf_ranker = TfidfRanker(inverted_index, N_PAGES, page_ranks, docs_length, True)

e = time.time()
print('Total preprocessing time:')
print(str(e - end) + ' seconds')

# print(docs_tokens)

def start_engine():
    setup_preferences()
    main_menu(USE_PAGE_RANK, USE_PSEUDO_RELEVANCE_FEEDBACK)

def main_menu():
    choice = gui.display_main_menu()

while 1:
    # start_engine()
    # main_menu()
    new_query()
