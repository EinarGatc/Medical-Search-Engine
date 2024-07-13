from collections import defaultdict
import SearchEngine.posting as posting
class Cache:
    def __init__(self, max_size):
        self.max_size = max_size
        self.cache = {}
        self.usage_count = defaultdict(int)

    def get(self, key):
        if key in self.cache:
            # Increment the usage count for the accessed key
            self.usage_count[key] += 1
            return self.cache[key]
        else:
            return None

    def put(self, key, value):
        if len(self.cache) >= self.max_size:
            # If the cache is full, remove the least used item
            self.evict()
        # Add the key-value pair to the cache
        self.cache[key] = value
        # Increment the usage count for the new key
        self.usage_count[key] += 1

    def evict(self):
        # Find the least used item by sorting the keys based on their usage count
        least_used_key = min(self.usage_count, key=self.usage_count.get)
        # Remove the least used item from the cache and usage count
        del self.cache[least_used_key]
        del self.usage_count[least_used_key]

def load_cache(load_size):
    '''Loads the cache from our cache.txt file.'''
    result = Cache(load_size)
    try:
        with open("cache.txt", "r") as file:
            count = 0
            line = file.readline()
            while line and count < load_size:
                data = line.split(":",2)
                key = data[0]
                usage_count = int(data[1])
                posting_list = posting.decode_posting_list(data[2])

                result.put(key, posting_list)
                result.usage_count[key] = usage_count 
                line = file.readline()
                count += 1
    except:
        pass
    return result
            

def save_cache(cache:Cache):
    '''Saves items currently in cache to our cache.txt file.'''
    usage_count = sorted(cache.usage_count.items(), key=lambda item: item[1], reverse=True)
    with open("cache.txt", "a+") as file:
        file.seek(0)
        file.truncate()
        for k, v in usage_count:
            posting_list = cache.cache[k].get()
            file.write(f"{k}:{v}:")
            for p in posting_list:
                file.write(posting.encode_posting(p))
            file.write("\n")