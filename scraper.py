import queue
visitedUrls = set()
contentHashes = dict()
validDomains = [
    "medlineplus.gov",
    "ncbi.nlm.nih.gov",
    "cdc.gov",
    "mayoclinic.org/patient-care-and-health-information",
    "merckmanuals.com/home",
    "nnlm.gov/guides",
    "www.testing.com",
    "ahrq.gov"
]

def RunScraper(loadState=False, saveFile="crawlerState.txt") -> None:
    frontier = InstantiateFrontier(loadState)

    while not frontier.empty():
        # Get Frontier
        new_url = frontier.get()

        # Check Content

        # Extract Links -> returns relative and absolute links

        # Relative to Absolute URLs -> returns all absolute links

        # Validate URL

        # Add URLs to Frontier

    pass

def InstantiateFrontier(loadState, saveFile) -> queue.Queue:
    frontier = queue.Queue()

    if loadState:
        pass
    else:
        for link in validDomains:
            frontier.put(link)

    return frontier