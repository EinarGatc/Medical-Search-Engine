class Posting:
    def __init__(self, d_id, frequency, fields=None, positions=None, tf_idf=0) -> None:
        self.d_id = d_id
        self.frequency = frequency  
        self.fields = fields
        self.positions = positions
        self.tf_idf = tf_idf

class PostingList:
    def __init__(self) -> None:
        self.postings = []
    
    def add(self, post: Posting):
        self.postings.append(post)
    
    def get(self):
        return self.postings
    
    def get_by_doc_id(self, doc_id):
        # find all postings with the given doc_id
        return [post for post in self.postings if post.d_id == doc_id]

def encode_posting(posting_obj:Posting) -> str:
    '''Encodes a posting object's information and returns it as a string.'''
    encoded_posting = f"{posting_obj.d_id}/{posting_obj.frequency}/{posting_obj.fields}/{posting_obj.positions}/{posting_obj.tf_idf}&"
    return encoded_posting

    

def decode_posting(posting_str:str) -> Posting:
    '''Decodes a string representation of a posting, into a Posting object.'''
    posting_fields = posting_str.strip().split("/")
    id = int(posting_fields[0])
    frequency = int(posting_fields[1])
    fields = posting_fields[2]
    fields = set() if fields == "set()" else set([tag.strip().strip("'") for tag in fields[1:len(fields)-1].split(',')])
    positions = posting_fields[3]
    positions = [int(position) for position in positions[1:len(positions)-1].split(',')]
    tf_idf = float(posting_fields[4])
    return Posting(id, frequency, fields, positions, tf_idf)

def decode_posting_list(postings_string:str) -> PostingList:
    '''Decodes a string representation of a posting, into a Posting object.'''
    result = PostingList()
    postings = postings_string.strip().split("&")
    postings = postings[0:len(postings)-1]
    for posting in postings:
        result.add(decode_posting(posting))
    return result

def print_posting(posting:Posting):
    '''Prints all Posting information.'''
    print(posting.d_id)
    print(posting.frequency)
    print(posting.fields)
    print(posting.positions)

if __name__ == "__main__":

    p1 = Posting(1,10,set(["a","b","c"]), [8,9,10])
    e1 = encode_posting(p1).strip("&")
    print(e1)
    d1 = decode_posting(e1)
    print_posting(d1)
