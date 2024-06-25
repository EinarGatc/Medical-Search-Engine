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

def run_scraper(loadState=False, saveFile) -> None:
    frontier = instantiate_frontier(loadState)

    while not frontier.empty():
        # Get Frontier
        new_url = frontier.get()


        # Check Content
        # Extract Links
        # Validate URL
        # Add URLs to Frontier

    pass

def instantiate_frontier(loadState, saveFile) -> queue.Queue:
    frontier = queue.Queue()

    if loadState:
        pass
    else:
        for link in valid_domains:
            frontier.put(link)

    return frontier