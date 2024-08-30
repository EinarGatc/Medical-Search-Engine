import queue
import time
from Parse import Tokenize, ComputeTokenFreq
from SimHashing import SimHash, ComputeSimHashSimilarity
from DataRetrieve import RetrieveUrlData, IsValid, SaveDocument
from Parse import Tokenize, ComputeTokenFreq
from ExtractLinks import ExtractLinks
from collections import defaultdict, deque

frontier = deque()
visitedUrls = set()
validUrls = set()
tokenCounts = defaultdict(int)
validDocuments = set()
contentHashes = set()
urlPathCount = dict()
traps = r"^.*\/commit.*$|^.*\/commits.*$|^.*\/tree.*$|^.*\/blob.*|^.*\signin.*|^.*\/login.*|^.*\/auth.*"
# keywords = [["diabetes"], ["covid"], ["flu"], ["influenza"], ["common", "cold"], ["asthma"], ["obesity"]]
keywords = [["diabetes"], ["covid"], ["influenza"], ["asthma"], ["obesity"]]

# validDomains = [r"^((.*\.)*medline\.gov)$", r"^((.*\.)*ncbi\.nlm\.nih\.gov)$", 
#                  r"^((.*\.)*cdc\.gov)$", r"^((.*\.)*mayoclinic\.org)$", 
#                  r"^((.*\.)*merckmanuals\.com)$", r"^((.*\.)*nnlm\.gov)$",
#                  r"^((.*\.)*www\.testing\.com)$", r"^((.*\.)*ahrq\.gov)$"]
validDomains = [r"^((.*\.)*cdc\.gov)$"]

def RunScraper(saveFile="crawlerState.txt", tokenLimit=5000000, tokenLower=100, tokenUpper=1000000, similarityThreshold=32) -> None:
    from SaveLoadCrawler import saveCrawler

    while frontier:
        # Get Frontier
        newUrl = frontier.popleft()
        if not pathThresholdCheck(newUrl):
            continue
        resp, status = RetrieveUrlData(newUrl)

        newLinks = Scraper(newUrl, resp, status, tokenLimit, tokenLower, tokenUpper, similarityThreshold)
        for link in newLinks:
            frontier.append(link)
        
        if newLinks:
            crawlData = {"frontier": frontier,
                         "visitedUrls": visitedUrls, 
                         "validUrls": validUrls,
                         "tokenCounts": tokenCounts,
                         "validDocuments": validDocuments,
                         "contentHashes": contentHashes}
            saveCrawler(crawlData)
        
        print(f"Current Url: {newUrl}, Token Count: {len(tokenCounts)}, Frontier: {len(frontier)}")
        time.sleep(.5)

def Scraper(newUrl, resp, status, tokenLimit, tokenLower, tokenUpper, similarityThreshold):
    if status == 200 and resp["content"] and resp["encoding"]:
        # check if the url is new
        if newUrl != resp["url"]:
            if resp["url"] in visitedUrls:
                return []
            visitedUrls.add(resp["url"])
            if not IsValid(resp["url"], validDomains, traps):
                return []

        # get the html content
        try:
            htmlContent = resp["content"].decode(resp["encoding"])
        except:
            return []
        # check that the page is not too big
        if len(htmlContent) > tokenLimit:
            return []
        
        tokens = Tokenize(htmlContent)
        totalTokens = len(tokens)
        
        if totalTokens < tokenLower or totalTokens > tokenUpper:
            return []
        
        tokenFrequencies = ComputeTokenFreq(tokens)
        simHashVector = SimHash(tokenFrequencies, 64)
        if not checkKeywords(tokenFrequencies):
            return []
        
        # Check Content
        if CheckUniqueContent(simHashVector, similarityThreshold):
            for k, v in tokenFrequencies.items():
                tokenCounts[k] += v
            contentHashes.add(simHashVector)
            SaveDocument(resp, len(validDocuments))
            validDocuments.add(resp["url"])
            
            newLinks = ExtractLinks(resp["url"], resp["content"], visitedUrls)

            finalLinks = []
            for link in newLinks:
                visitedUrls.add(link)
                if pathThresholdCheck(link) and IsValid(link, validDomains, traps):
                    validUrls.add(link)
                    finalLinks.append(link)
            
            # Add URLs to Frontier
            return finalLinks
        else:
            pathThresholdUpdate(resp["url"])
        return []
    return []

# def InstantiateFrontier(loadState, saveFile):
#     # baseFrontier = ["https://medlineplus.gov", "https://ncbi.nlm.nih.gov/", 
#     #                 "https://www.cdc.gov/", "https://www.mayoclinic.org/", 
#     #                 "https://www.merckmanuals.com/", "https://www.nnlm.gov/",
#     #                 "https://www.testing.com/", "https://www.ahrq.gov"]
#     baseFrontier = ["https://www.cdc.gov/"]
#     if loadState:
#         loadCrawler()
#     else:
#         for link in baseFrontier:
#             frontier.append(link)
#             visitedUrls.add(link)
#             validUrls.add(link)

def CheckUniqueContent(newHash, similarityThreshold=32) -> bool:
    if newHash in contentHashes:
        return False
    
    for currentHash in contentHashes:
        simHashValue = ComputeSimHashSimilarity(newHash, currentHash)
        if simHashValue > similarityThreshold:
            return False  # Similar content found, content is not unique

    return True

def pathThresholdUpdate(url):
    baseUrl = url.split('?', 1)[0].strip()

    if baseUrl not in urlPathCount:
        urlPathCount[baseUrl] = 1
    else:
        urlPathCount[baseUrl] += 1

def pathThresholdCheck(url, threshold = 10):
    baseUrl = url.split('?', 1)[0].strip()
    
    if baseUrl in urlPathCount and urlPathCount[baseUrl] >= threshold:
        return False
        
    return True

def checkKeywords(tokenFrequencies):
    for kwList in keywords:
        flag = True
        for kw in kwList:
            if kw not in tokenFrequencies:
                flag = False
        if flag:
            return True
    return False

if __name__ == "__main__":
    RunScraper(similarityThreshold=62)
    print("Finished")