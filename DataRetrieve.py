from scraper import visitedUrls, validDomains
from SaveLoadCrawler import saveCrawler, loadCrawler
import requests
import json
import re
from bs4 import BeautifulSoup

def RetrieveUrlData(url : str) -> dict | int:
    """Fetch the raw HTML content from a given URL.
    
    Parameters
    ----------
    url : string
        a string that is a URL which will be used to fetch HTML data
    
    Returns
    -------
    dict
        a dictionary object that contains the url, content, encoding
    int
        the status of the data retrieval
    """
    try:
        page = requests.get(url)
    except:
        return {}, 404
    
    if not page.ok:
        return {}, page.status_code
    
    return {"url" : page.url, "content": page.content.decode(page.encoding), "encoding" : page.encoding}, page.status_code


def TrapDetection(url : str) -> bool | str:
    """Detect and avoid crawler traps that could cause infinite loops.
    
    Parameters
    ----------
    url : string
        a string that is a url which will be used to determine if the link is a trap
    
    Returns
    -------
    boolean
        a boolean value that tells whether or not the url is a trap
    string
        a string that outputs the reason the url is marked as not valid
    """
    statusError = ""
    queryPattern = "\?.*"
    domainPattern = "(?:https?:\/\/)(?:www\.)?(?:\w+\.?)+"
    newUrl = re.split(queryPattern, url)[0]
    try:
        domain = re.search(domainPattern,url)[0].split("//")[1].replace("www.","")
    except:
        return True, "Could not find domain"
        
    if newUrl in visitedUrls:
        return True, newUrl+" was already visited"
    elif domain not in validDomains:
        return True, domain+" is not in list of valid domains"
    return False, ""

def SaveDocument(doc : dict) -> None:
    """Store the processed document in a database or file system.
    
    Parameters
    ----------
    doc : dict
        a dictionary object that contains the url, content, and html type
    
    Returns
    -------
    None
    """
    fileName = "Documents.json"
    newJSON = []

    #Check if json file exists
    try:
        with open(fileName, "r") as file:
            newJSON = json.load(file)
    except:
        with open(fileName, "w") as file:
            file.write('[\n]')

    #Appends new data to json
    newJSON.append(doc)

    #Write to and format json
    with open(fileName, "w") as file:
        json.dump(newJSON, file, indent=4, separators=(',',': '))


#This function is only used for testing purposes
def run():
    url = "https://medlineplus.gov/druginformation.html"
    doc, status = RetrieveUrlData(url)
    trap, error = TrapDetection(url)
    if trap:
        print(error)
        return
    if status == 200:
        print(f'Successfully saved {doc["url"]}')
        visitedUrls.add(doc["url"])
        SaveDocument(doc)
    else:
        print("Error Retrieving URL Data")

if __name__ == "__main__":
    loadCrawler()
    run()
    saveCrawler()