import Scraper
from SaveLoadCrawler import loadCrawler

class Worker:
    def run(self, loadState=False):
        self.InstantiateFrontier(loadState)
        Scraper.RunScraper(similarityThreshold=62)
    
    def InstantiateFrontier(self, loadState):
        # baseFrontier = ["https://medlineplus.gov", "https://ncbi.nlm.nih.gov/", 
        #                 "https://www.cdc.gov/", "https://www.mayoclinic.org/", 
        #                 "https://www.merckmanuals.com/", "https://www.nnlm.gov/",
        #                 "https://www.testing.com/", "https://www.ahrq.gov"]
        baseFrontier = ["https://www.cdc.gov/flu/", "https://www.cdc.gov/diabetes/", 
                        "https://www.cdc.gov/asthma/", "https://www.cdc.gov/obesity/",
                        "https://www.cdc.gov/covid/"]
        if loadState:
            loadCrawler()
        else:
            for link in baseFrontier:
                Scraper.frontier.append(link)
                Scraper.visitedUrls.add(link)
                Scraper.validUrls.add(link)

if __name__ == "__main__":
    worker = Worker()
    worker.run(loadState=True)
