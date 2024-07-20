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
    # for i in range(len(tokens)):
    #     words = i.split()
    #     tokens[i] = stemmer2.stem(tokens[i])

    for i in range(len(tokens)):
        words = tokens[i].split() # handle bigrams
        stemmed_words = [stemmer2.stem(word) for word in words]
        tokens[i] = " ".join(stemmed_words)

    return tokens


def stem_word(word):
    '''Stems a token using the Porter2Stemmer and returns token.'''
    return stemmer2.stem(word)


def hybrid_stemming_tokens(tokens):
    '''Stems each token using a hybrid of SnowballStemmer & LancasterStemmer and returns the list of tokens.'''
    return [hybrid_stemming(token) for token in tokens]


if __name__ ==  "__main__":
    # tokens = ["learning", "gaps", "gas", "ties", "cries", "stress", "agreed", "feed", "fished", "pirating", "falling", "dripping", "hoping", "Lopes,"]
    # print(tokens)
    # stemming_tokens(tokens)
    # print(tokens)
    
    # tokens = "the and".split()
    # print([stemmer2.stem(t) for t in tokens])
    # print([stemmer2.stem(t) for t in tokens])




    # Testing Stemmer with Bigrams

    tokens1 = ['Imagined', 'In', 'the', 'heart', 'of', 'the', 'ancient', 'forest', 'where', 'the', 'canopy', 'was', 'so', 'thick', 'that', 'sunlight', 'barely', 'touched', 'the', 'ground', 'lived', 'a', 'girl', 'named', 'Elara', 'She', 'had', 'grown', 'up', 'among', 'the', 'towering', 'trees', 'and', 'whispering', 'leaves', 'her', 'only', 'companions', 'the', 'creatures', 'of', 'the', 
    'wood', 'and', 'the', 'distant', 'echo', 'of', 'her', 'mother', 's', 'lullabies', 'One', 'evening', 'as', 'the', 'sky', 'blazed', 'with', 'the', 'colors', 'of', 'dusk', 'Elara', 'stumbled', 'upon', 'a', 'hidden', 'glade', 'In', 'its', 'center', 'stood', 'a', 'tree', 'unlike', 'any', 'other', 'its', 'bark', 'shimmering', 'with', 'an', 'ethereal', 'glow', 'Intrigued', 'she', 'approached', 'and', 'found', 'a', 'small', 'intricately', 'carved', 'box', 'nestled', 'among', 'its', 'roots', 'As', 'she', 'opened', 'it', 'a', 'soft', 'golden', 'light', 'enveloped', 'her', 'and', 'she', 'heard', 'a', 'voice', 'gentle', 'yet', 'commanding', 'You', 'have', 'been', 'chosen', 'Elara', 'to', 'awaken', 'the', 'ancient', 'guardians', 'and', 'restore', 'balance', 'to', 'our', 'world', 'Thus', 'began', 'her', 'journey', 'one', 'that', 'would', 'take', 'her', 'far', 'beyond', 'the', 'familiar', 'confines', 'of', 
    'her', 'forest', 'home', 'and', 'into', 'realms', 'of', 'magic', 'and', 'danger', 'she', 'had', 'never', 'imagined', 'danger', 'she', 'never', 'imagined', 'In the', 'the heart', 'heart of', 'of the', 'the ancient', 'ancient forest', 'forest where', 'where the', 'the canopy', 'canopy was', 'was so', 'so thick', 'thick that', 'that sunlight', 'sunlight barely', 
    'barely touched', 'touched the', 'the ground', 'ground lived', 'lived a', 'a girl', 'girl named', 'named Elara', 'Elara She', 'She had', 'had grown', 'grown up', 'up among', 'among  the', 'the towering', 'towering trees', 'trees and', 'and whispering', 'whispering leaves', 'leaves her', 'her only', 'only companions', 'companions the', 'the creatures', 'creatures of', 'of the', 'the wood', 'wood and', 'and the', 'the distant', 'distant echo', 'echo of', 'of her', 'her mother', 'mother s', 's lullabies', 'lullabies One', 'One evening', 'evening as', 'as the', 'the sky', 'sky blazed', 'blazed with', 'with the', 'the colors', 'colors of', 'of dusk', 'dusk Elara', 'Elara stumbled', 'stumbled upon', 'upon a', 'a hidden', 
    'hidden glade', 'glade In', 'In its', 'its center', 'center stood', 'stood a', 'a tree', 'tree unlike', 'unlike any', 'any other', 'other its', 'its bark', 'bark shimmering', 'shimmering with', 'with an', 'an ethereal', 'ethereal glow', 'glow Intrigued', 'Intrigued she', 'she approached', 'approached and', 'and found', 'found a', 'a small', 'small intricately', 'intricately carved', 'carved box', 'box nestled', 'nestled among', 'among its', 'its roots', 'roots As', 'As she', 'she opened', 'opened it', 'it a', 'a soft', 'soft golden', 'golden light', 'light enveloped', 'enveloped her', 'her and', 'and she', 'she heard', 'heard a', 'a voice', 'voice gentle', 'gentle yet', 'yet commanding', 'commanding You', 'You have', 'have been', 'been chosen', 'chosen Elara', 'Elara to', 'to awaken', 'awaken the', 'the ancient', 'ancient guardians', 'guardians and', 'and restore', 'restore balance', 'balance to', 'to our', 'our world', 'world Thus', 'Thus began', 'began her', 'her journey', 'journey one', 'one that', 'that would', 'would take', 'take her', 'her far', 'far beyond', 'beyond the', 'the familiar', 'familiar confines', 'confines of', 'of her', 'her forest', 'forest home', 'home and', 'and into', 'into realms', 'realms of', 'of magic', 'magic and', 'and danger', 'danger she', 'she had', 'had never', 'never imagined', 'imagined danger', 'danger she', 'she never', 'never imagined']


    tokens2 = ['Imagined', 'In', 'the', 'heart', 'of', 'the', 'ancient', 'forest']
    tokens3 = ['In the', 'the heart', 'heart of', 'of the', 'the ancient', 'ancient forest']

    stemmed1 = stemming_tokens(tokens1)
    print(stemmed1)

    stemmed2 = stemming_tokens(tokens2)
    print(stemmed2)

    stemmed3 = stemming_tokens(tokens3)
    print(stemmed3)