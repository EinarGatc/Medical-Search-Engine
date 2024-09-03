import nltk
import threading
nltk.download('stopwords')
from nltk.corpus import stopwords
import stemming as stemming
from index_data import get_query_postings, query_postings_to_id, get_files, get_urls
from intersect import intersect_query_terms
from posting import decode_posting_list
from cache import Cache, load_cache, save_cache
from score import SearchScore
import time
filepath1 = "/Users/egatchal/Medical-Search-Engine/index-data/indexFinal.txt"
filepath2 = "/Users/egatchal/Medical-Search-Engine/index-data/index_urls.txt"
filepath3 = "/Users/egatchal/Medical-Search-Engine/index-data/indexFinalSeek.txt"
filepath4 = "/Users/egatchal/Medical-Search-Engine/index-data/index_list.txt"

# filepath1 = r"C:\Users\Jason\Medical-Search-Engine\search-engine\index-data\index-data\indexFinal.txt"
# filepath2 = r"C:\Users\Jason\Medical-Search-Engine\search-engine\index-data\index-data\index_urls.txt"
# filepath3 = r"C:\Users\Jason\Medical-Search-Engine\search-engine\index-data\index-data\indexFinalSeek.txt"
# filepath4 = r"C:\Users\Jason\Medical-Search-Engine\search-engine\index-data\index-data\index_list.txt"


# scoreWeights = {"TF-IDF": .5, "PR": .2, "TW": .1, "WP": .1, "PS": .1}
scoreWeights = {"TF-IDF": .4, "PR": .2, "TW": .1, "WP": .2, "PS": .1}
seek_lock = threading.Lock()
query_lock = threading.Lock()
query_postings = dict()
query_cache = load_cache(500)


def worker_thread_index_search(token, file_index, query_lock, seek_lock):
    '''Seeks for a token using the search_index_index function.'''
    posting_list = query_cache.get(token)
    if not posting_list:
        posting_list = search_index_index(token, file_index, seek_lock)
    with query_lock:
        if posting_list and token not in query_postings:
            query_postings[token] = posting_list

def perform_index_search_on_query(trimmed_query, index_file):
    '''
    Searches for all tokens in a query using multithreading and index_index search.\n
    All searched tokens that are not tokens of the query will be stored in a set.
    '''
    threads = []
    searched_tokens = set()
    for token in trimmed_query:
        if token not in searched_tokens:
            searched_tokens.add(token)
            thread = threading.Thread(target=worker_thread_index_search, args=(token, index_file, query_lock, seek_lock))
            thread.start()
            threads.append(thread)
    
    for thread in threads:
        thread.join()
    

def convert_seek_into_dict():
    '''
    Gathers index_seek.txt information and returns it as a dictionary.\n
    (Uses pre-determined variables like filepath3 as index_seek.txt)
    '''
    result = dict()
    with open(filepath3) as seek_file:
        # with open("/Users/shika/Assignment3/index_seek.txt") as seek_file:
        line = seek_file.readline()
        while(line):
            value = line.split(":", 1)
            token = value[0]
            seek = int(value[1])
            result[token] = seek
            line = seek_file.readline()
    return result

def convert_index_list_into_dict():
    '''Gathers index_list.txt information and returns it as a dictionary.'''
    result = dict()
    with open(filepath4) as index_list_file:
        # with open("/Users/shika/Assignment3/index_list.txt") as index_list_file:
        line = index_list_file.readline()
        while(line):
            value = line.split(":", 1)
            token = int(value[0])
            url = value[1].strip()
            result[token] = url
            line = index_list_file.readline()
    return result

def convert_index_urls_into_dict():
    '''Gathers index_urls.txt information and returns it as a dictionary.'''
    result = dict()
    with open(filepath2) as index_urls:
        # with open("/Users/shika/Assignment3/index_urls.txt") as index_urls:
        line = index_urls.readline()
        while(line):
            value = line.split(":", 1)
            token = int(value[0])
            url = value[1].strip()
            result[token] = url
            line = index_urls.readline()
    return result

def convert_pagerank_into_dict(filename):
    d = {}
    with open(filename, "r+") as f:
        line = f.readline()
        while line:
            data = line.split(":", 1)
            dID, page_rank = int(data[0]), float(data[1])
            d[dID] = page_rank
            line = f.readline()
    return d

# data that is small enough to store in memory
index_index = convert_seek_into_dict()
index_list = convert_index_list_into_dict()
index_urls = convert_index_urls_into_dict()
page_rank = convert_pagerank_into_dict("/Users/egatchal/Medical-Search-Engine/PRS.txt")
# page_rank = convert_pagerank_into_dict(r"c:\Users\Jason\Downloads\PRS.txt")
stop_words = set(stopwords.words("english"))

def remove_stopwords(query) -> list:
    '''Removes all stopwords from the query and returns a list of query words.'''
    trimmed_query = []
    if query:
        for word in query.split():
            if word.lower() not in stop_words:
                trimmed_query.append(word)
    return trimmed_query

def print_top5_urls(urls):
    '''Prints top 5 occurring URLs gathered from a user's query.'''
    for i, url in enumerate(urls, 1):
        if i > 5:
            break
        print(f"{i}: {url}")

def get_top5_urls(urls):
    '''Returns a list of the top 5 URLs gathered from user's query.'''
    result = []
    for i, url in enumerate(urls, 1):
        if i > 5:
            break
        result.append(url)
    return result

def process_query(query) -> list:
    '''Trims and stems the query and returns a list of tokens in the query'''
    token_list = query.lower().split(" ")
    if len(token_list) <= 3 or get_query_proportion(token_list) <= 0.35:
        stemming.stemming_tokens(token_list)
        return token_list
    
    trimmed_query = remove_stopwords(query)
    stemming.stemming_tokens(trimmed_query)
    return trimmed_query

def start_query(query, index_file):
    result = find_query(query, index_file)
    return result

def find_query(query, index_file):
    '''Gathers and returns the intersecting URLs from the query tokens.'''
    
    starttime = time.time()
    trimmed_query  = process_query(query)
    add_bigrams_trigrams(trimmed_query)
    # print(f"P1 Time: {time.time()-starttime}")
    # perform_binary_search_on_query(trimmed_query, index_file)
    perform_index_search_on_query(trimmed_query, index_file)
    # print(f"P2 Time: {time.time()-starttime}")
    query_intersection = intersect_query_terms(query_postings)

    # print(f"P3 Time: {time.time()-starttime}")
    docs_ranked = get_query_score(trimmed_query, query_intersection)

    # print(f"P4 Time: {time.time()-starttime}")
    urls = get_urls(docs_ranked, index_urls)
    
    # print(f"P5 Time: {time.time()-starttime}")
    # urls = get_top5_urls(urls)

    return urls

def add_bigrams_trigrams(trimmed_query):
    newTokens = []
    for tokens in nltk.bigrams(trimmed_query):
        newTokens.append(" ".join(tokens))
    for tokens in nltk.trigrams(trimmed_query):
        newTokens.append(" ".join(tokens))
    for newToken in newTokens:
        trimmed_query.append(newToken)

def convert_seek_into_dict():
    '''Gathers index_seek.txt information and returns it as a dictionary.'''
    result = dict()
    with open("index_seek.txt") as seek_file:
        line = seek_file.readline()
        while(line):
            value = line.split(":")
            token = value[0]
            seek = int(value[1])
            result[token] = seek
            line = seek_file.readline()
    return result

def search_index_index(token, index_file, seek_lock):
    '''Searches index using a tokens posting location to retrieve information.'''
    if token in index_index:
        seek_pos = index_index[token]
        with seek_lock:
            index_file.seek(seek_pos)
            line = index_file.readline()
        data = line.split(':', 1)
        return decode_posting_list(data[1])
    return None

def get_query_proportion(token_list) -> float:
    '''Checks the proportion of real tokens (real tokens are NOT stop words) and returns that value.'''
    count = sum(1 for token in token_list if token.lower() not in stop_words)
    return count / len(token_list)


def pos_to_weight(positions, percent=0.25):
    """
    Calculate the positional weight based on the positions of the tokens.
    
    Parameters:
    - positions: List of positions where the token appears in the document.
    - threshold: Position threshold to determine importance.

    Returns:
    - A proportion representing the positional weight.
    """
    if not positions:
        return 0
    
    count = 0
    threshold = positions[len(positions)-1] * percent
    for pos in positions:
        if pos <= threshold:
            count += 1
        else:
            break  # Break out of the loop as soon as the condition is no longer met
    weight = count / len(positions)

    return weight


def get_query_score(query_list, query_postings) -> list:
    '''Returns a total query score from the intersecting pages of the query tokens.\n
    (based on token occurrence and total size of the indexer)
    '''
    proximityScore = SearchScore(query_postings)
    scores = dict()
    lengths = dict()
    query_freq = to_dict(query_list)
    scores = dict()
    for term in query_list:
        if term in query_postings:
            postings = query_postings[term].get()
            for post in postings:
                if post not in scores:
                    scores[post.d_id] = 0 
                    lengths[post.d_id] = 0

                tf_idf = post.tf_idf
                freq = query_freq[term]
                tag_weight = tag_to_weight(post.fields)
                pos_weight = pos_to_weight(post.positions)
                scores[post.d_id] += scoreWeights["TF-IDF"] * tf_idf  + scoreWeights["PR"] * page_rank[post.d_id] + scoreWeights["TW"] * tag_weight + scoreWeights["WP"] * pos_weight + scoreWeights["PS"] * proximityScore[post.d_id]
                lengths[post.d_id] += 1
           
    for k, v in scores.items():
        scores[k] = v / lengths[k]

    tuple_list = [(key, value) for key,value in scores.items()]
    tuple_list.sort(key=lambda x: x[1], reverse=True)

    return tuple_list

def to_dict(query_list) -> dict:
    '''
    Tranforms a token list into a dictionary with its value of occurrences in that query\n
    Example: ["to", "be", "or", "not", "to", "be"] -> {"to": 2, "be":2, "or":1, "not":1}
    '''
    query_freq = dict()
    for elem in query_list:
        if elem not in query_freq:            
            query_freq[elem] = 1
        else:
            query_freq[elem] += 1
    return query_freq

def tag_to_weight(tag_set) -> float:
    '''Calculates the total weight of a token by it's tags in a page.'''
    if not tag_set:
        return 0.0

    tag_weights = {
        'title': 1.0,
        'header': 0.9,
        'h1': 0.9,
        'h2': 0.8,
        'h3': 0.8,
        'h4': 0.5,
        'h5': 0.4,
        'h6': 0.3,
        'strong': 0.8,
        'b':0.8
    }
    
    maxValue = 0
    for tag in tag_set:
        maxValue = max(maxValue, tag_weights[tag])

    return maxValue

def cosine_sim_score(query_len, post, value) -> float:
    '''Calculates a weight score to use for ranking intersecting pages.'''
    score = (post.frequency * value) / query_len
    return score

if __name__ == "__main__": 
    # # At least the following queries should be used to test your retrieval:
    index1 = filepath1
    # # # index1 = "/Users/shika/Assignment3/index.txt"
    with open(index1, "r+") as f1:
        query = input("Enter query (q to quit): ")
        while query.strip() != "q":  # Check if input is empty or only whitespace
            starttime = time.time()
            urls = find_query(query, f1)
            print_top5_urls(urls)
            endtime = time.time()
            print(f"Time: {endtime-starttime}, Size: {len(urls)}")
            
            for k, v in query_postings.items():
                query_cache.put(k, v)
            query_postings.clear()

            query = input("Enter query (q to quit): ")
    save_cache(query_cache)
    print("END")

    # index1 = "/Users/egatchal/Desktop/Projects/index_data/index.txt"
    # # index1 = "/Users/shika/Assignment3/index.txt"
    # with open(index1, "r+") as f1:
    #     for query in stop_words:
    #         starttime = time.time()
    #         urls = find_query(query, f1)
    #         endtime = time.time()
    #         print(f"Time: {endtime-starttime}")
    #         print_top5_urls(urls)
    #         for k, v in query_postings.items():
    #             query_cache.put(k, v)
    #         query_postings.clear()
    # save_cache(query_cache)
    # print("END")


