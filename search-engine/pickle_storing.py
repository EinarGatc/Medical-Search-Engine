# from scraper import valid_set, visited_set, content_hashes, content, content_file, ics_subdomains, global_frequencies, url_hashes, url_path_count
import pickle
import os
from index import Posting

def pickle_data(data, filename):
    """Serialize data to a file using the Pickle library.

    Parameters
    ----------
    crawl_data : dict
        a dict of containers that store data on previously crawled websites
    filename : str
        the file name of where the pickled data will be stored
    """
    with open(filename, "wb") as file:
        pickle.dump(data, file)

def load_pickled_data(filename):
    """Deserialize data from a pickled file.

    Parameters
    ----------
    crawl_data : dict

    Returns
    -------
    bool
        a bool indicating whether the data was successfully deserialized
    """
    try:
        with open(filename, "rb") as content:
            p = pickle.load(content)
        return p
    except FileNotFoundError: 
        return None


def get_pickle_file_size(filename):
    return os.path.getsize(filename) / 1000
