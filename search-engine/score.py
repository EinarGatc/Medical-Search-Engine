import math
import numpy as np
import time
import threading
from intersect import intersect_query_terms
from posting import Posting, PostingList

documentScore = dict()
query_lock = threading.Lock()

def GetProximityScore(doc,arr,lock):
    a = []
    for i in range(len(arr)-1):
        n = []
        for j in arr[i]:
            n.append(FindDistanceAscending(j,arr[i+1]))
        a.append(n)

    scores = []
    for i in range(len(a[0])):
        n = i
        score = 0
        for j in range(len(a)):
            score += a[j][n][0]
            n = a[j][n][1]
        scores.append(score)
    with lock:
        documentScore[doc] = min(scores)**-1

def GetPhraseScore(doc,arr,lock):
    last = set()
    score = 0
    if len(arr) < 1:
        return 0
    elif len(arr) == 1:
        return len(arr)
    
    for num in arr[len(arr)-1]:
        last.add(num)
    
    count = 0
    while len(arr)-2-count >= 0:
        new = set()
        for num in arr[len(arr)-2-count]:
            if num+1 in last:
                if len(arr)-2-count == 0:
                    score += 1
                new.add(num)
        last = new.copy()
        count += 1

    with lock:
        documentScore[doc] = score

def SearchScore(trimmedQuery, queryIntersection):
    queryPositions = dict()
    for term in trimmedQuery:
        if term in queryIntersection:
            postings = queryIntersection[term].get()
            for post in postings:
                if post.d_id not in documentScore:
                    queryPositions[post.d_id] = []
                    documentScore[post.d_id] = 0 
                queryPositions[post.d_id].append(post.positions)
    threads = []
    for doc in queryPositions:
        arr = queryPositions[doc]
        GetPhraseScore(doc,arr,query_lock)
        # thread = threading.Thread(target=GetPhraseScore, args=[doc,arr,query_lock])
        # thread.start()
        # threads.append(thread)

    # for thread in threads:
    #     thread.join()
    return documentScore

def FindDistanceAscending(num, arr):
    min = math.inf
    l = 0
    r = len(arr)-1
    m = int((r+l)/2)
    while l <= r:
        if min > arr[m]-num:
            min = arr[m]-num
        if arr[m] == num:
            return min, m
        elif num > arr[m]:
            l = m+1
        else:
            r = m-1
        m = int((r+l)/2)
    
    if arr[m] < num:
        try:
            min = arr[m+1]-num
            m = m+1
        except:
            min = math.inf
            m = -1
    return min, m

def FindDistanceDescending(num, arr):
    min = math.inf
    l = 0
    r = len(arr)-1
    m = int((r+l)/2)
    while l <= r:
        if min > num-arr[m]:
            min = num-arr[m]
        if arr[m] == num:
            return min, m
        elif num > arr[m]:
            l = m+1
        else:
            r = m-1
        m = int((r+l)/2)
    
    if arr[m] > num:
        try:
            min = arr[m-1]-num
            m = m-1
        except:
            min = math.inf
            m = -1
    return min, m

if __name__ == "__main__":
    query_postings = dict()
    query_postings["d"] = PostingList()
    query_postings["a"] = PostingList()
    query_postings["l"] = PostingList()
    
    for i in range(200000):
        query_postings["d"].add(Posting(i,3,None,[1,3,5]))
        query_postings["a"].add(Posting(i,3,None,[2,4,9]))
        query_postings["l"].add(Posting(i,3,None,[6,7,10]))
    
    # query_postings["d"].add(Posting(0,3,None,[1,3,5]))
    # query_postings["a"].add(Posting(0,3,None,[2,4,9]))
    # query_postings["l"].add(Posting(0,3,None,[6,7,10]))

    # query_postings["d"].add(Posting(1,3,None,[1,4,10]))
    # query_postings["a"].add(Posting(1,3,None,[2,8,12]))
    # query_postings["l"].add(Posting(1,3,None,[3,9,13]))

    # query_postings["d"].add(Posting(2,3,None,[1,56,101]))
    # query_postings["a"].add(Posting(2,3,None,[2,57,102]))
    # query_postings["l"].add(Posting(2,3,None,[3,58,103]))

    query_intersection = intersect_query_terms(query_postings)
    start = time.time()
    scores = SearchScore(["d","a","l"],query_intersection)
    print(time.time()-start)
    # print(scores)
