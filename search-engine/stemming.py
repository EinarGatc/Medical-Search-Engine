import re
from nltk.stem import WordNetLemmatizer, SnowballStemmer, LancasterStemmer
from porter2stemmer import Porter2Stemmer
stemmer1 = SnowballStemmer('english')
stemmer2 = LancasterStemmer()
stemmer3 = Porter2Stemmer()
# stemmer3 = WordNetLemmatizer()

def hybrid_stemming(token, length_threshold = 10):
    '''
    Stems the token based on the length of the token that is passed in.\n
    For example: Tokens larger than 10 use LancasterStemmer & tokens smaller use SnowballStemmer.
    '''
    word = token[0]
    tag = token[1]
    # if re.search(r"[\-\.]", word):
    #     return (stemmer3.lemmatize(word), tag)
    if len(word) <= length_threshold:
        return (stemmer1.stem(word), tag)
    else:
        return (stemmer2.stem(word), tag)
        
def stem_token(token):
    '''Stems the token using the LancasterStemmer.'''
    return stemmer2.stem(token)

# def stemming_tokens_with_tags(tokens):
#     for i in range(len(tokens)):
#         tokens[i][0] = stemmer2.stem(tokens[i][0])

def stemming_tokens(tokens):
    '''Stems each token using the Porter2Stemmer and returns the list of tokens.'''
    for i in range(len(tokens)):
        tokens[i] = stemmer2.stem(tokens[i])

def stem_word(word):
    '''Stems a token using the Porter2Stemmer and returns token.'''
    return stemmer2.stem(word)


def hybrid_stemming_tokens(tokens):
    '''Stems each token using a hybrid of SnowballStemmer & LancasterStemmer and returns the list of tokens.'''
    return [hybrid_stemming(token) for token in tokens]


if __name__ ==  "__main__":
    tokens = ["learning", "gaps", "gas", "ties", "cries", "stress", "agreed", "feed", "fished", "pirating", "falling", "dripping", "hoping", "Lopes,"]
    print(tokens)
    stemming_tokens(tokens)
    print(tokens)
    
    tokens = "the and".split()
    print([stemmer2.stem(t) for t in tokens])
    print([stemmer2.stem(t) for t in tokens])