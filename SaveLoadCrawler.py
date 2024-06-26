import pickle
from scraper import visitedUrls, contentHashes, validDomains

def saveCrawler():
    state = {
        "urls_visited":visitedUrls,
        "content_hashes":contentHashes,
        "domains_valid":validDomains
    }

    with open('state.pkl', 'wb') as file:
        pickle.dump(state, file)


def loadCrawler():
    with open('state.pkl', 'rb') as file:
        state = pickle.load(file)

    visitedUrls = state["urls_visited"]
    contentHashes = state["content_hashes"]
    validDomains = state["domains_valid"]

