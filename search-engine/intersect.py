from posting import PostingList
# input is a list of LISTS of doc_ids that different tokens appears in
def intersect_query_terms(query_postings):
    '''Returns a set of documents that the query terms have in common.'''
    result = dict()
    if not query_postings:
        return result

    key_order = []
    min_key = min(query_postings, key=lambda k: len(query_postings[k].get())) # finds key with the least number of postings
    min_list = [p for p in query_postings[min_key].get()] # list of postings (# of postings is the smallest)
    key_order.append(min_key)

    for p in min_list:
        result[p.d_id] = PostingList()
        result[p.d_id].add(p)

    for k, v in query_postings.items():
        copy = min_list[::]
        if k == min_key:
            continue
        
        # key_order.append(k)

        posting_list = v.get()
  
        index1 = 0
        index2 = 0

        # only look through ids in the min list
        idsToPop = []
        while index1 < len(min_list) and index2 < len(posting_list):
            id1 = min_list[index1].d_id 
            id2 = posting_list[index2].d_id
            if id1 == id2:
                result[id1].add(posting_list[index2])
                index1 += 1
                index2 += 1
            elif id1 < id2:
                min_list.pop(index1)
                idsToPop.append(id1)
            else:
                index2 += 1
        
        while index1 < len(min_list):
            p = min_list.pop(index1)
            idsToPop.append(p.d_id)
        
        if len(min_list) == 0: # do not delete anything (ensures result hopefully)
            min_list = copy
        else:
            key_order.append(k)
            for id in idsToPop:
                result.pop(id)
    
    final_result = dict()

    for k, v in result.items():
        for i, p in enumerate(v.get()):
            token = key_order[i]
            if token not in final_result:
                final_result[token] = PostingList()
            final_result[token].add(p)

    return final_result
                

# Testing:

if __name__ == "__main__":
    
    query_postings1 = [[1,2,3,4,5,6,7,8], [3,5,9], [2,3,5,9,4]]
    intersect_postings1 = intersect_query_terms(query_postings1)
    print(intersect_postings1) # [3,5]
    
    query_postings2 = [[10, 11, 12, 13], [11, 14, 15], [10, 11, 16]]
    intersect_postings2 = intersect_query_terms(query_postings2)
    print(intersect_postings2) # [11]
    
    query_postings3 = [[20, 21, 22, 23], [21, 22, 24, 25], [20, 21, 22, 23, 26]]
    intersect_postings3 = intersect_query_terms(query_postings3)
    print(intersect_postings3) # [21,22]
    
    query_postings4 = [[30, 31, 32], [31, 33, 34], [31, 32, 35]]
    intersect_postings4 = intersect_query_terms(query_postings4)
    print(intersect_postings4) # [31]
    
    query_postings5 = [[40, 41, 42, 43, 44], [42, 43, 45, 46], [41, 42, 43, 47]]
    intersect_postings5 = intersect_query_terms(query_postings5)
    print(intersect_postings5) # [42,43]
    


    
