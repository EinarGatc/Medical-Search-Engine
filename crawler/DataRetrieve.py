import requests
import json
import re
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse

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
        page = requests.get(url, timeout=1)
    except:
        return {}, 404
    
    if not page.ok:
        return {}, 404
    
    return {"url" : page.url, "content": page.content, "encoding" : page.encoding}, page.status_code

def IsValid(url, validDomains, traps) -> bool:
    """Check if the URL is valid against the acceptable set of URL's.

    Parameters
    ----------
    url : str
        a URL that is checked for validity
    validDomains : list[str]
        a list of domains as regex

    Returns
    -------
    bool
        a bool that indicates if the URL is valid
    """
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        
        if parsed.scheme not in set(["http", "https"]):
            return False
        
        # for domain in validDomains:
        if not any(re.match(domain, parsed.netloc) for domain in validDomains):
            return False
        
        if not url.isascii():
            return False

        repeatingDirs = r"^.*?(/.+?/).*?\1.*$|^.*?/(.+?/)\2.*$"
        
        if re.match(traps, url):
            return False
        
        if re.match(repeatingDirs, url):
            return False
        
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|mpg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1|war|img|apk|ff"
            + r"|thmx|mso|arff|rtf|jar|csv|bib|java|m|cc|odp|class|mexglx"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz|pov|sh)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        return False


def SaveDocument(resp : dict, docNum : int) -> None:
    """Store the processed document in a database or file system.
    
    Parameters
    ----------
    doc : dict
        a dictionary object that contains the url, content, and html type
    
    Returns
    -------
    None
    """
    fileName = f"document{docNum}.json"
    folderPath = 'documents'
    htmlContent = resp["content"].decode(resp["encoding"])

    jsonData = {'url': resp['url'], 
                'content': htmlContent,
                'encoding': resp['encoding']}
    
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
        
    filePath = os.path.join(folderPath, fileName)

    with open(filePath, "w") as file:
        json.dump(jsonData, file, indent=4)


#This function is only used for testing purposes
# def run():
#     url = "https://medlineplus.gov/druginformation.html"
#     doc, status = RetrieveUrlData(url)
#     trap, error = TrapDetection(url)
#     if trap:
#         print(error)
#         return
#     if status == 200:
#         print(f'Successfully saved {doc["url"]}')
#         visitedUrls.add(doc["url"])
#         SaveDocument(doc)
#     else:
#         print("Error Retrieving URL Data")\
    

# Hearty's Tests
def TestRetrieveURLData(url):
    dictionary, status = RetrieveUrlData(url)

    for value in dictionary.values():
        assert value != ()

    for value in dictionary.values(): # should print url, html content, and encoding
        print(value)
        print("-------------------------------------------------------------------------------------------------------------------")

    print("Test cases passed")

def TestSaveDocument(url):
    file_path = 'Documents.json'

    dictionary, status = RetrieveUrlData(url)
    SaveDocument(dictionary)

    assert os.path.isfile(file_path), "The JSON file was not created."
    
    # Load and check the JSON contents
    with open(file_path, 'r') as file:
        data = json.load(file)

    assert data is not None, "The JSON file is empty or invalid."
    assert isinstance(data, list), "The JSON file does not contain a list."
    assert len(data) > 0, "The JSON list is empty."

    print("All Test Cases Passed")


if __name__ == "__main__":
    # loadCrawler()
    # run()
    # saveCrawler()


    # For running TestRetrieveURLData, test ONE URL at a time. Comment out so only one TestRetrieveURLData is active.

    # TestRetrieveURLData("https://www.cdc.gov/index.html")
    # TestRetrieveURLData("https://www.ncbi.nlm.nih.gov/")


    TestSaveDocument("https://www.cdc.gov/index.html") 
    TestSaveDocument("https://www.ncbi.nlm.nih.gov/")

    # Manually check is Documents.json was generated and a dict containing(url, content, encoding) for both urls exist in the Documents.json

