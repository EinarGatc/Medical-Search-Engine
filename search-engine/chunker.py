from posting import PostingList, encode_posting
# chonk chonk

def save_index_chunk(index:dict[str, PostingList], indexList:dict[str, str], index_urls:dict[int, str], file1, file2, file3):
    '''
    Saves a string containing page location and token count to to the index.txt file.\n
    Example: {token_exists_in_page} : {token_occurrence_count}
    '''
    with open(file1, "a+") as f:
        f.seek(0)
        f.truncate()
        for token, posting_list in index.items():
            entry = f"{token}: "
            
            for post in posting_list.get():
                entry += encode_posting(post)

            entry += "\n"
            f.write(entry)
    
    with open(file2, "a+") as f:
        f.seek(0)
        f.truncate()
        for k, v in indexList.items():
            entry = f"{k}: {v}\n"
            f.write(entry)
    
    with open(file3, "a+") as f:
        f.seek(0)
        f.truncate()
        for k, v in index_urls.items():
            entry = f"{k}: {v}\n"
            f.write(entry)

def chunk_index(index, index_list, index_urls, chunk):
    '''
    A Proxy function that saves the index in chunks by calling save_index_chunk.'''
    save_index_chunk(index, index_list, index_urls, f"index{chunk}.txt", f"index{chunk}_list.txt", f"index{chunk}_urls.txt")