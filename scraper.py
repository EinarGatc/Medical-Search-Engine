import queue
visitedUrls = set()
contentHashes = dict()
valid_domains = [
    "medlineplus.gov",
    "ncbi.nlm.nih.gov",
    "cdc.gov",
    "mayoclinic.org/patient-care-and-health-information",
    "merckmanuals.com/home",
    "nnlm.gov/guides",
    "www.testing.com",
    "ahrq.gov"
]

def run_scraper(load_state=False) -> None:
    

    pass

def instantiate_frontier(load_state) -> queue.Queue:
    frontier = queue.Queue()
    
    if load_state:
        pass
    else:
        for link in valid_domains:
            frontier.put(link)

    return frontier