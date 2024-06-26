from scraper import visitedUrls
from SaveLoadCrawler import saveCrawler, loadCrawler
import requests
import json
import re
from bs4 import BeautifulSoup

def RetrieveUrlData(url) -> dict | int:
    """Fetch the raw HTML content from a given URL.
    
    Parameters
    ----------
    url : string
        a string that is a URL which will be used to fetch HTML data
    
    Returns
    -------
    JSON
        a JSON object that contains the url, content, encoding, and status
    """
    try:
        page = requests.get(url)
    except:
        return {}, 404
    
    if not page.ok:
        return {}, page.status_code
    
    return {"url" : page.url, "content": page.content.decode(page.encoding), "encoding" : page.encoding}, page.status_code


def TrapDetection(url) -> bool:
    """Detect and avoid crawler traps that could cause infinite loops.
    
    Parameters
    ----------
    url : string
        a string that is a url which will be used to determine if the link is a trap
    
    Returns
    -------
    boolean
        a boolean value that tells whether or not the url is a trap
    """
    pattern = "\?.*"
    newUrl = re.split(pattern, url)[0]
    if newUrl in visitedUrls:
        return True
    return False

def SaveDocument(doc) -> None:
    """Store the processed document in a database or file system.
    
    Parameters
    ----------
    doc : JSON
        a JSON object that contains the url, content, and html type
    
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

def run():
    url = "https://www.wikipedia.com/"
    doc, status = RetrieveUrlData(url)
    if TrapDetection(url):
        return
    if status == 200:
        print(doc["url"])
        visitedUrls.add(doc["url"])
        SaveDocument(doc)
    else:
        print("Error Retrieving URL Data")

if __name__ == "__main__":
    loadCrawler()
    run()
    saveCrawler()