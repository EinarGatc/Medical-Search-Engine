from posting import decode_posting_list, print_posting, PostingList
import json

def get_query_postings(filepath, queries):
    '''Returns the location of a token (from a query) in the index.txt file.'''
    count = 0
    query_postings = {query: PostingList() for query in queries}
    # query_postings = dict()
    
    with open(filepath, "r") as f:
        while count < len(queries):
            line = f.readline()
            if not line:
                break

            data = line.split(":", 1)
            token = data[0]

            if token not in queries:
                continue     
            
            count += 1
            postings = decode_posting_list(data[1])
            query_postings[token] = postings
        
    return query_postings

def query_postings_to_id(query_postings):
    '''Returns a dict of query tokens and the set of pages they exist in.'''
    query_postings_id = dict()
    for k, v in query_postings.items():
        ids = set()
        for p in v.get():
            ids.add(p.d_id)
        query_postings_id[k] = ids
    return query_postings_id

def get_files(posting_ids, index_list):
    '''Gather and return list of filepaths from posting_ids in index_list.txt file.'''
    filepaths = []
    
    for id in posting_ids:
        filepaths.append(index_list[id])
        
    return filepaths

def get_urls(docs_ranked, index_urls):
    '''Gathers and returns a list of URLs from filepath.'''
    urls = []

    for id, score in docs_ranked:
        urls.append(index_urls[id])

    return urls

if __name__ == "__main__":
    query = get_query_postings("index.txt", set(["Classes", "The", "Transformative", "Irvine", "2020ICS"]))
    print(query)
    query_id = query_postings_to_id(query)

    print(query_id)