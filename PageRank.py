import os, json, sys
from collections import defaultdict
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse
from scipy.sparse import csr_matrix, linalg
import numpy as np
linkCount = 0
adjacencyList = defaultdict(list)
visited = set()
docs = dict()

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
            docs[url] = len(docs)
            
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
    CombineAdjacencyLists(adjListFolderPath)

def OffloadAdjacencyList(offloadCount, folderPath):
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)

    filePath = os.path.join(folderPath, f"AdjList{offloadCount}.txt")

    with open(filePath, "w+") as f:
        for k, v in adjacencyList.items():
            f.write(f"{k}:{v}\n")

def CombineAdjacencyLists(folderPath):
    # filePath = os.path.join(folderPath, f"AdjListFinal.txt")
    filePath = "AdjListFinal.txt"
    finalFile = open(filePath, "w+")

    for adjListPath in GetDocuments(folderPath):
        with open(adjListPath, "r+") as f:
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

def pageRank(threshold, beta) :
    A = ConvertAdjListToMatrix(len(docs), "/Users/egatchal/Medical-Search-Engine/AdjListFinal.txt", "/Users/egatchal/Medical-Search-Engine/AdjMatrixFinal.txt")
    arr = np.array(A, dtype=float)
    
    s = []
    n = len(A)
    
    for i in range(n):
        s.append(np.sum(arr[:,i]))

    M = arr 

    for i in range(n):
        M[:,i] = M[:,i] / s[i]

    rNew = (1.0+np.zeros([len(M), 1])) / len(M)
    c = (1.0-beta) * rNew
    rPrev = rNew

    for i in range(0,1000):
        rNew = beta * np.matmul(M, rPrev) + c
        diff = np.sum(abs(rNew-rPrev))
        if diff < threshold:
            break
        rPrev = rNew

    return rNew[:,0]

def ConvertAdjListToMatrix(numDocs, adjListFilePath, adjMatrixFilePath):
    fileAdjMatrix = open(adjMatrixFilePath, "w+")
    matrix = [[0 for j in range(numDocs)] for i in range(numDocs)]

    with open(adjListFilePath, "r+") as file:

        data = file.readline().split(":", 1)
        node, neighbors = int(data[0]), set([int(n) for n in data[1][1:-2].split(",")])

        for i in range(numDocs):
            for j in range(numDocs):
                if i == j or (i == node and j in neighbors):
                    matrix[i][j] = 1
                    fileAdjMatrix.write(f"1 ")
                    
                else:
                    fileAdjMatrix.write("0 ")
            fileAdjMatrix.write("\n")
            if i == node:
                data = file.readline().split(":", 1)
                if data[0]:
                    node, neighbors = int(data[0]), set([int(n) for n in data[1][1:-2].split(",")])
    
    denseMatrix = np.array(matrix, dtype=float)
    # rows, cols = np.nonzero(denseMatrix)
    # values = denseMatrix[rows, cols]
    # sparseMatrix = csr_matrix((values, (rows, cols)), shape=denseMatrix.shape)
    fileAdjMatrix.close()

    return denseMatrix

def ConvertAdjListToTelMatrix(numDocs, adjListFilePath, adjMatrixFilePath):
    fileAdjMatrix = open(adjMatrixFilePath, "w+")
    matrix = [[0 for j in range(numDocs)] for i in range(numDocs)]

    with open(adjListFilePath, "r+") as file:

        data = file.readline().split(":", 1)
        node, neighbors = int(data[0]), set([int(n) for n in data[1][1:-2].split(",")])

        for i in range(numDocs):
            prob = 1.0 / (len(neighbors)+1) if i == node else 1
            for j in range(numDocs):
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

if __name__ == "__main__":
    CreateAdjacencyList("/Users/egatchal/Desktop/Projects/DEV", "/Users/egatchal/Medical-Search-Engine/AdjListFolder", maxDocs=10)
    pageRankScores = pageRank(0.00000000001, 0.8)
    print(pageRankScores)