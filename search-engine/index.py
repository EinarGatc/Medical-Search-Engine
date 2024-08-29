import os
from parse import parse_document, compute_token_frequencies, compute_token_frequencies2
import stemming
from important_text import get_tokens_with_tags, get_text_from_json, get_tokens_without_tags
import pickle_storing
from posting import Posting, PostingList, encode_posting, decode_posting, decode_posting_list
from math import log
from chunker import chunk_index
from bs4 import BeautifulSoup
from simhashing import sim_hash, compute_sim_hash_similarity
import time
from collections import defaultdict
import math

id_to_document = dict()
content_hashes = set()
id_normalize_tfidf = defaultdict(float)
# returns list of batches
def get_batches(documents, num_batches = 3):
    '''Splits documents into separate batches equally.'''
    docs_len = len(documents)
    base_size = docs_len // num_batches
    remainder = docs_len % num_batches
    
    batches = []
    start_index = 0
    
    for i in range(num_batches):
        batch_size = base_size + (1 if i < remainder else 0)
        batch = documents[start_index:start_index + batch_size]
        batches.append(batch)
        start_index += batch_size
        
    return batches

def build_index(documents, batch_size):
    '''Builds an inverted index from list of documents and returns a dict of updated information.'''
    chunk = 1
    id_to_document = dict()
    index = dict()
    index_urls = dict()
    
    # 1. get a batch of documents
    # 2. parse and stem batch, and add into index
    # 3. save index onto disk (index1.txt)
    # 4. clear index

    
    batch_list = get_batches(documents, batch_size)
    n = 1
    for batch in batch_list:
        for d in batch:
            data = get_text_from_json(d)
            text = BeautifulSoup(data["content"], "html.parser")
            
            stemmed_tokens = get_tokens_without_tags(text)
            tokens_dict = compute_token_frequencies2(stemmed_tokens)
            
            # hash_vector = sim_hash(tokens_dict)
            # if not check_content(hash_vector, similarity_threshold=60): # content unique get links
            #     continue
            
            id_to_document[n] = d
            index_urls[n] = data["url"]
            # content_hashes.add(hash_vector)

            stemmed_token_tags_dict = get_tokens_with_tags(text)
            stemmed_tokens = compute_token_frequencies(stemmed_tokens)
            
            for k, v in stemmed_tokens.items():
                if k not in index:
                    index[k] = PostingList()
                if k in stemmed_token_tags_dict:
                    index[k].add(Posting(n, v[0], stemmed_token_tags_dict[k], v[1]))
                else:
                    index[k].add(Posting(n, v[0], set(), v[1]))
            
            print(f"Document #: {n}, Document: {d}, Tokens: {len(index)}")
            n += 1
            
        index = dict(sorted(index.items()))
        chunk_index(index, id_to_document, index_urls, chunk)
        index.clear()
        id_to_document.clear()
        index_urls.clear()
        chunk += 1
    
    merge_indexes(chunk-1, len(documents))
    get_tfidf()
    # return index

def build_index2(documents):
    '''Builds an inverted index from list of documents and returns a dict of updated information.'''
    index = dict()
    for n, d in enumerate(documents, 1):
        id_to_document[n] = d 
        text = get_text_from_json(d)
        tokens = get_tokens_without_tags(text)
        stemmed_tokens = stemming.porter2_stemming_tokens(tokens)
        token_frequencies = compute_token_frequencies2(stemmed_tokens)
        for k, v in token_frequencies.items():
            if k not in index:
                index[k] = PostingList
            index[k].append(Posting(n, v))
        print(f"Document #: {n}, Document: {d}, Tokens: {len(index)}")
    return index

def check_content(new_hash_vector, similarity_threshold = 64):
    """Check if the new content set is exact or approximately similar to existing sets.
    
    Parameters
    ----------
    new_hash_vector : tuple
        a tuple containing the hash of a URL's tokens
    similarity_threshold : int
        an arbitrary value set to 64 for a similarity score threshold

    Return
    ------
    bool
        a bool indicating how similar the content is to the threshold\n
        (Very Similar = False, Not Similar = True)
    """

    # Check for exact match first
    if new_hash_vector in content_hashes:
        return False  # Exact match found, content is not unique

    # Check for approximate similarity
    for hash_vector in content_hashes:
        if compute_sim_hash_similarity(new_hash_vector, hash_vector) > similarity_threshold:
            return False  # Similar content found, content is not unique

    return True  # Content is unique

def get_documents(folder_path, flag = True, file_count = 10):
    '''Gathers and returns a list of filepaths from a folder passed in.'''
    documents = []
    for root, _, files in os.walk(folder_path):
        if flag and len(documents) > file_count:
            break
        for filename in files:
            if flag and len(documents) > file_count:
                break
            documents.append(os.path.join(root, filename))
    return documents
    
def get_stats():
    '''Loads and prints statistical data from the .txt files using our Pickle storing system.'''
    p1 = pickle_storing.load_pickled_data("index_data.pickle")
    p2 = pickle_storing.load_pickled_data("id_doc_data.pickle")

    print("Number of Indexed Documents:", len(p2))
    print("Number of Unique Words:", len(p1))
    print("Size of Index (in Kilobytes):", pickle_storing.get_pickle_file_size("index_data.pickle"))

def save_index(index:dict[str, PostingList]):
    '''
    Saves a string containing page location and token count to to the index.txt file.\n
    Example: {token_exists_in_page} : {token_occurrence_count}
    '''
    with open("index.txt", "a+") as f:
        f.seek(0)
        f.truncate()
        
        for token, posting_list in index.items():
            entry = f"{token}: "
            
            for post in posting_list.get():
                entry += encode_posting(post)

            entry += "\n"
            f.write(entry)
    
    with open("index_list.txt", "a+") as f:
        f.seek(0)
        f.truncate()
        for k, v in id_to_document.items():
            entry = f"{k}: {v}\n"
            f.write(entry)

def get_size_of_index(index_dict) -> int:
    '''Gets the size of the index file.'''
    return len(index_dict)

def index_chunker(index) -> int:
    '''Split the index file into three separate chunks for efficiency.'''
    chunk_size = int(get_size_of_index(index)/3) + 1
    return chunk_size

def write_tf_idf(file, file_out, len_of_docs, r = 10000):
    '''Adds a TF-IDF score to our index for efficiency.'''
    file_out.seek(0)
    value = file_out.readline()
    line = value.split(":", 1)
    token = line[0]
    postings_list = line[1]
    postings_list = decode_posting_list(postings_list)
    len_of_postings = len(postings_list.get())
    new_list = []

    file.write(f"{token}: ")
    for posting in postings_list.get():
        tf = 1 + log(posting.frequency)
        idf = log(len_of_docs/float(len_of_postings))
        tf_idf = tf * idf
        posting.tf_idf = tf_idf
        new_list.append(posting)
        file.write(encode_posting(posting))
        id_normalize_tfidf[posting.d_id-1] += tf_idf**2
        
    file.write("\n")

def merge_indexes(batches, len_of_docs) -> None:
    '''Merges all our .txt files (or partial indexes) into one file called index.txt.'''
    list_of_files = []
    list_of_files_index = []
    list_of_files_urls = []

    for i in range(batches):
        list_of_files.append(open(f"index{i+1}.txt"))
        list_of_files_index.append(open(f"index{i+1}_list.txt"))
        list_of_files_urls.append(open(f"index{i+1}_urls.txt"))

    files_to_close = list(list_of_files)
    list_of_tokens = []    
    for index in list_of_files:
        value = index.readline()
        line = value.split(":",1)
        token = line[0]
        posting_list = line[1]
        list_of_tokens.append((token,posting_list))

    with open('index.txt', 'a+') as file:
        with open('entry.txt', 'w+') as file_out:

            file.seek(0)
            file.truncate()

            file_out.seek(0)
            file_out.truncate()

            last_token = None

            while(list_of_files):
                current_position = file_out.tell()
                min_token, min_index = list_of_tokens[0], 0 #get the next token to be added
                length = len(list_of_tokens)

                for i in range(1, length):
                    value = list_of_tokens[i]
                    if value[0] < min_token[0]:
                        min_token, min_index = value, i  
                
                if last_token and last_token == min_token[0]: # same token
                    file_out.seek(current_position-1)
                    file_out.write(min_token[1].strip())
                else: # new token
                    if last_token:
                        write_tf_idf(file, file_out, len_of_docs, 2)
                        file_out.seek(0)
                        file_out.truncate()
                    entry = f"{min_token[0]}: {min_token[1].strip()}\n"
                    file_out.write(entry) # write the new entry
                
                last_token = min_token[0]
                value = list_of_files[min_index].readline()

                if value == "":
                    list_of_tokens.pop(min_index)
                    list_of_files[min_index].close()
                    list_of_files.pop(min_index)
                else:
                    line = value.split(":",1)
                    token = line[0]
                    posting_list = line[1]
                    list_of_tokens[min_index] = (token, posting_list)
        
    with open("index_list.txt", "a+") as f:
        f.seek(0)
        f.truncate()
        
        count = 1
        for file in list_of_files_index:
            line = file.readline()
            while(line):
                f.write(f"{count}:{line.split(':', 1)[1]}")
                line = file.readline()
                count += 1
            file.close()
    
    with open("index_urls.txt", "a+") as f:
        f.seek(0)
        f.truncate()
        
        count = 1
        for file in list_of_files_urls:
            line = file.readline()
            while(line):
                f.write(f"{count}:{line.split(':', 1)[1]}")
                line = file.readline()
                count += 1
            file.close()

def get_tfidf():
    indexFile =  open('index.txt', 'r+')
    seekFile = open('indexFinalSeek.txt', 'w+') 
    newIndexFile = open('indexFinal.txt', 'w+')
    
    for k, v in id_normalize_tfidf.items():
        id_normalize_tfidf[k] = math.sqrt(v)
    
    line = indexFile.readline()
    while line:
        data = line.split(':', 1)
        token, tokenPostings = data[0], decode_posting_list(data[1])

        seekFile.write(f"{token}: {newIndexFile.tell()}\n") # writes the byte to seek to
        newIndexFile.write(f"{token}: ")
        for posting in tokenPostings.get():
            if id_normalize_tfidf[posting.d_id] != 0.0:
                posting.tf_idf /= id_normalize_tfidf[posting.d_id]
            
            newIndexFile.write(encode_posting(posting))
        newIndexFile.write("\n")
        
        line = indexFile.readline()
    
    indexFile.close()
    seekFile.close()
    newIndexFile.close()
            
def convert_seek_into_dict():
    '''Gathers information from the index_seek.txt file and returns that as a dictionary.'''
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


if __name__ == "__main__":
    documents = get_documents("/Users/egatchal/Medical-Search-Engine/crawler/CDC_Documents", False, 10) # For Pookiebear
    # documents = get_documents("/Users/shika/Desktop/DEV", False) # For Jeff
    documents = get_documents("Medical-Search-Engine\developer", True) # harpy

    index = build_index(documents, 3)
    save_index(index)

    # starttime = time.time()
    # build_index(documents, 4)
    # endtime = time.time()
    # print(f"Time: {endtime-starttime}")
    # print("END")

    # result = binary_search(["software", "machine", "0"])
    # print("print result", result)
    
    # index = build_index(["/Users/egatchal/Desktop/Assignments/CS121/DEV/chenli_ics_uci_edu/0dd51496522b853a3cd23b185ecdd452cb906d3ec82819f2a4c3bce2d39cefe4.json"])
    # save_index(index)
    # print("END")
    # test_query = "cristina lopes"
    # # test_query = "machine learning"
    # # test_query = "ACM"
    # # test_query = "master of software engineering"

    # trimmed_query = query.remove_stopwords(test_query)
    # print("After removing stopwords:", trimmed_query)

    # result = stemming.porter2_stemming_tokens(trimmed_query) # porter2stemming works kinda
    # print("After stemming query words:", result)

        
    # test_list = query.find_token_index_list("index_folder", result)
    # for x in test_list:
    #     print(x)

    # count = 0
    # for k, v in index.items():
    #     if count < 10:
    #         for p in v:
    #             print(f"Token: {k}, Doc_ID: {p.d_id}, Frequency: {p.frequency}, Fields: {p.fields}")
    #     count += 1
    
    # get_stats()