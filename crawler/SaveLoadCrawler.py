import pickle
import Scraper

def saveCrawler(crawlData):
    with open('state.pkl', 'wb') as file:
        pickle.dump(crawlData, file)


def loadCrawler():
    with open('state.pkl', 'rb') as file:
        state = pickle.load(file)
        Scraper.frontier = state.get("frontier")
        Scraper.visitedUrls = state.get("visitedUrls")
        Scraper.contentHashes = state.get("validUrls")
        Scraper.tokenCounts= state.get("tokenCounts")
        Scraper.validDocuments = state.get("validDocuments")
        Scraper.contentHashes = state.get("contentHashes")
    print(f"{len(Scraper.frontier)}{len(Scraper.visitedUrls)}\n{len(Scraper.contentHashes)}\n{len(Scraper.tokenCounts)}\n{len(Scraper.validDocuments)}\n{len(Scraper.contentHashes)}\n")

