from pickle_storing import load_pickled_data, get_pickle_file_size
import index

def get_stats():
    '''Loads and prints statistical data from the .txt files using our Pickle storing system.'''
    p1 = load_pickled_data("index_data.pickle")
    p2 = load_pickled_data("id_doc_data.pickle")

    print("Number of Indexed Documents:", len(p2))
    print("Number of Unique Words:", len(p1))
    print("Size of Index:", get_pickle_file_size("index_data.pickle"))

if __name__ == "__main__":
    get_stats()