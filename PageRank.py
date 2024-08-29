import os, json, sys
from collections import defaultdict
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse
import scipy.sparse as sp
import numpy as np

linkCount = 0
adjacencyList = defaultdict(list)
visited = set()
docs = dict() # maps url to documentID
documents = dict()

def CreateAdjacencyList(folderPath, adjListFolderPath, restrictDocs = True, maxDocs = 10000, maxSize = 1000000):
    clearFolder(adjListFolderPath)
    offloadCount = 0
    for docuementPath in GetDocuments(folderPath):
        if restrictDocs and len(visited) == maxDocs:
            break

        data = GetJsonData(docuementPath)
        text = BeautifulSoup(data["content"], "html.parser")
        url = data["url"]

        if url not in visited:
            visited.add(url)

            if url not in docs:
                docs[url] = len(docs)

            documents[docs[url]] = len(documents)
            adjacentLinks = GetUrls(url, text)
            
            for link in adjacentLinks:
                if link not in docs:
                    docs[link] = len(docs)
                adjacencyList[docs[url]].append(docs[link]) 

        if sys.getsizeof(adjacencyList) > maxSize:
            OffloadAdjacencyList(offloadCount, adjListFolderPath)
            adjacencyList.clear()
            offloadCount += 1 
        
    
    OffloadAdjacencyList(offloadCount, adjListFolderPath)
    adjacencyList.clear()
    offloadCount += 1 
    CombineAdjacencyLists(adjListFolderPath, offloadCount)
    SaveDocUrlToDocID(adjListFolderPath)
    

def SaveDocUrlToDocID(adjListFolderPath):
    filePath = os.path.join(adjListFolderPath, f"urlToDocID.txt")
    with open(filePath, "w+") as f:
        for k, v in docs.items():
            f.write(f"{k}:{v}\n")

def OffloadAdjacencyList(offloadCount, folderPath):
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)

    filePath = os.path.join(folderPath, f"AdjList{offloadCount}.txt")

    with open(filePath, "w+") as f:
        for k, v in adjacencyList.items():
            f.write(f"{k}:{v}\n")

def CombineAdjacencyLists(folderPath, offloadCount):
    # filePath = os.path.join(folderPath, f"AdjListFinal.txt")
    filePath = "AdjListFinal.txt"
    finalFile = open(filePath, "w+")

    for i in range(offloadCount):
        with open(f"{folderPath}/AdjList{i}.txt", "r+") as f:
            line = f.readline()
            while line:
                finalFile.write(line)
                line = f.readline()
    
    finalFile.close()

def GetDocuments(folderPath):
    '''Gathers and returns a list of filepaths from a folder passed in.'''
    documents = []
    for root, _, files in os.walk(folderPath):
        for filename in files:
            documentPath = os.path.join(root, filename)
            yield documentPath

def GetJsonData(documentPath) -> str:
    '''Reads file passed in and returns its content in HTML form.'''
    with open(documentPath, 'rb') as file:
        jsonData = json.load(file)
    return jsonData

def GetUrls(baseUrl, text):
    """Extracts links from a string of HTML content
    
    Parameters
    ----------
    baseUrl
        the URL of the webpage the HTML content is from

    htmlString
        a string of HTML content
    
    visitedUrls
        a set of visited urls
    
    Returns
    -------
    list
        a list of extracted links
    """
    newLinks = set()
    for tag in text.find_all('a'): 
        if tag.get('href'):
            newLink = tag['href']
            absoluteLink = CreateAbsoluteUrl(baseUrl, newLink)
            if absoluteLink and absoluteLink not in newLinks: 
                newLinks.add(absoluteLink)

    return newLinks

def CreateAbsoluteUrl(baseUrl, newUrl):
    """Joins url to base URL to create absolute url
    
    Parameters
    ----------
    baseUrl
        the URL of the webpage the HTML content is from
        
    newURL
        url to transform into absolute url
    
    Returns
    -------
    list
        absolute url
    """
    newUrl = newUrl.split('#', 1)[0].strip().lower()
    try:
        absoluteUrl = urljoin(baseUrl, newUrl)
        absoluteUrl = Normalize(absoluteUrl)
    except:
        return None

    return absoluteUrl

def Normalize(url):
    """Normalize the URL by removing fragments and query parameters, lowercasing, etc."""
    parsedUrl = urlparse(url)
    normalizedUrl = urlunparse((
        parsedUrl.scheme,
        parsedUrl.netloc.lower(),
        parsedUrl.path.rstrip('/'),
        parsedUrl.params,
        parsedUrl.query,  # keep the query part
        ''  # remove the fragment
    ))
    return normalizedUrl

def PageRank(M, threshold, beta) :
    n = M.shape[0]
    rNew = (1.0+np.zeros([n, 1])) / n
    c = (1.0-beta) * rNew
    rPrev = rNew

    for i in range(0,1000):
        print(M.shape)
        print(rPrev.shape)
        rNew = beta * (M @ rPrev) + c
        diff = np.sum(abs(rNew-rPrev))
        if diff < threshold:
            break
        rPrev = rNew

    return rNew[:,0]

def ConvertAdjListToMatrix(adjListFilePath, adjMatrixFilePath):
    values = []
    rows = []
    cols = []

    with open(adjListFilePath, "r+") as file:
        data = file.readline().split(":", 1)
        while data[0]:
            node, neighbors = int(data[0]), set([int(n) for n in data[1][1:-2].split(",")])
            
            prob = 1.0 / len(neighbors)
            for i in neighbors:
                values.append(prob)
                rows.append(node)
                cols.append(i)
        
            data = file.readline().split(":", 1)

    n = max(max(rows), max(cols)) + 1
    sparseMatrix = sp.coo_matrix((values, (cols, rows)), shape=(n,n))
    return sparseMatrix

def ConvertAdjListToTelMatrix(n, adjListFilePath, adjMatrixFilePath):

    fileAdjMatrix = open(adjMatrixFilePath, "w+")
    matrix = np.zeros((n,n))
    print("Created matrix")
    with open(adjListFilePath, "r+") as file:

        data = file.readline().split(":", 1)
        node, neighbors = int(data[0]), set([int(n) for n in data[1][1:-2].split(",")])

        for i in range(n):
            prob = 1.0 / (len(neighbors)+1) if i == node else 1
            for j in range(n):
                if i == j or (i == node and j in neighbors):
                    matrix[i][j] = prob
                    fileAdjMatrix.write(f"{prob} ")
                else:
                    fileAdjMatrix.write("0 ")
            fileAdjMatrix.write("\n")
        
            if i == node:
                data = file.readline().split(":", 1)
                if data[0]:
                    node, neighbors = int(data[0]), set([int(n) for n in data[1][1:-2].split(",")])
    
    # denseMatrix = np.array(matrix, dtype=float)
    # rows, cols = np.nonzero(denseMatrix)
    # values = denseMatrix[rows, cols]
    # sparseMatrix = csr_matrix((values, (rows, cols)), shape=denseMatrix.shape)
    fileAdjMatrix.close()

    return matrix

def clearFolder(folderPath):
    for root, _, files in os.walk(folderPath):
        for filename in files:
            documentPath = os.path.join(root, filename)
            os.remove(documentPath)

def SavePageRank(pageRankScores, filePath):
    with open(filePath, "w+") as f:
        for k, v in documents.items():
            f.write(f"{v+1}:{pageRankScores[k]}\n")

def CreatePageRank(folderPathDocs, folderPathAdjList, filePathPRS):
    CreateAdjacencyList(folderPathDocs, folderPathAdjList, filePathPRS)
    print("Create Adajacency List")
    M = ConvertAdjListToMatrix("/Users/egatchal/Medical-Search-Engine/AdjListFinal.txt", "/Users/egatchal/Medical-Search-Engine/AdjMatrixFinal.txt")
    print("Convert Adjancency List to Matrix")
    pageRankScores = PageRank(M, 0.00000000001, 0.8)
    print("Finished Creating PageRank Scores")
    SavePageRank(pageRankScores, filePathPRS)
    print("Finished Saving PageRank Scores")

if __name__ == "__main__":
    CreatePageRank("/Users/egatchal/Medical-Search-Engine/crawler/CDC_Documents", "/Users/egatchal/Medical-Search-Engine/AdjListFolder","/Users/egatchal/Medical-Search-Engine/PRS.txt")