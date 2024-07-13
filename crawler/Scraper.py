import queue
import time
from Parse import Tokenize, ComputeTokenFreq
from SimHashing import SimHash, ComputeSimHashSimilarity
from DataRetrieve import RetrieveUrlData,  IsValid
from Parse import Tokenize, ComputeTokenFreq
from ExtractLinks import ExtractLinks

visitedUrls = set()
validUrls = set()

contentHashes = set()
traps = []
tokenCount = 0

validDomains = [r"^((.*\.)*medline\.gov)$", r"^((.*\.)*ncbi\.nlm\.nih\.gov)$", 
                 r"^((.*\.)*cdc\.gov)$", r"^((.*\.)*mayoclinic\.org)$", 
                 r"^((.*\.)*merckmanuals\.com)$", r"^((.*\.)*nnlm\.gov)$",
                 r"^((.*\.)*www\.testing\.com)$", r"^((.*\.)*ahrq\.gov)$"]

def RunScraper(loadState=False, saveFile="crawlerState.txt", tokenLimit=5000000, tokenLower=100, tokenUpper=1000000, similarityThreshold=32) -> None:
    frontier = InstantiateFrontier(loadState, saveFile)
    while not frontier.empty():
        # Get Frontier
        newUrl = frontier.get()
        resp, status = RetrieveUrlData(newUrl)

        newLinks = Scraper(newUrl, resp, status, tokenLimit, tokenLower, tokenUpper, similarityThreshold)
        for link in newLinks:
            frontier.put(link)
                
        print(f"Current Url: {newUrl}, Token Count: {tokenCount}")
        time.sleep(.5)

def Scraper(newUrl, resp, status, tokenLimit, tokenLower, tokenUpper, similarityThreshold):
    if status == 200 and resp["content"]:
        if newUrl != resp["url"]:
            if resp["url"] in visitedUrls:
                return []
            visitedUrls.add(resp["url"])
        
        htmlContent = resp["content"].decode(resp["encoding"])
        
        if len(htmlContent) > tokenLimit:
            return []
        
        tokens = Tokenize(htmlContent)
        totalTokens = len(tokens)
        
        if totalTokens < tokenLower or totalTokens > tokenUpper:
            return []
        
        tokenFrequencies = ComputeTokenFreq(tokens)
        simHashVector = SimHash(tokenFrequencies, 64)
        
        # Check Content
        if CheckUniqueContent(simHashVector, similarityThreshold):
            contentHashes.add(simHashVector)
            # save the document
            # Extract Links and Save Page Content if unique
            newLinks = ExtractLinks(resp["url"], resp["content"], visitedUrls)
            
            # Validate URL
            finalLinks = []
            for link in newLinks:
                visitedUrls.add(link)
                if IsValid(link, validDomains):
                    validUrls.add(link)
                    finalLinks.append(link)
            
            # Add URLs to Frontier
            return finalLinks
        
        return []

def InstantiateFrontier(loadState, saveFile) -> queue.Queue:
    frontier = queue.Queue()
    baseFrontier = ["https://medlineplus.gov", "https://ncbi.nlm.nih.gov/", 
                    "https://www.cdc.gov/", "https://www.mayoclinic.org/", 
                    "https://www.merckmanuals.com/", "https://www.nnlm.gov/",
                    "https://www.testing.com/", "https://www.ahrq.gov"]
    if loadState:
        pass
    else:
        for link in baseFrontier:
            frontier.put(link)
            visitedUrls.add(link)
            validUrls.add(link)

    return frontier

def CheckUniqueContent(newHash, similarityThreshold=32) -> bool:
    if newHash in contentHashes:
        return False
    
    for currentHash in contentHashes:
        if ComputeSimHashSimilarity(newHash, currentHash) > similarityThreshold:
            return False  # Similar content found, content is not unique

    return True

if __name__ == "__main__":
    RunScraper()