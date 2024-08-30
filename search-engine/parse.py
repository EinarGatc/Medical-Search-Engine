import re
import nltk

def is_alnum(char) -> bool:
    '''Checks if char passed in as an argument is alphanumeric.'''
    pattern = r"[a-zA-Z0-9]"
    return re.match(pattern, char)
    
def parse_document(text):
    """Tokenizes the input text file
    
    Parameters
    ----------
    doc : str 
        the text file path to read from
    
    Returns
    -------
    list
        a list of tokens read from the input file
    """
    tokens = []
    token = ""
    
    for c in text:
        if (is_alnum(c)): # check if character is ascii and add to current working token
            token += c
        else:
            if token:
                tokens.append(token) # if token is not empty string add to tokens
                token = ""
    
    if token: # if last token is not empty string add to tokens
        tokens.append(token)

    # generate a list of bigrams (in tuple form by default)
    textBigrams = list(nltk.bigrams(tokens))

    textTrigrams = list(nltk.trigrams(tokens))

    gramList = []

    for tuple in textBigrams: # change tuples into string
        bigramStr = " ".join(tuple)
        gramList.append(bigramStr)

    for tuple in textTrigrams:
        trigramStr = " ".join(tuple)
        gramList.append(trigramStr)
        
    
    # add bigrams to current list of tokens
    tokens.extend(gramList)

    return tokens

def compute_token_frequencies(tokens):
    """Compute the frequency of tokens
    
    Parameters
    ----------
    tokens : list
        list of tokens
    
    Returns
    -------
    dict
        a dictionary containing:
        key: token

        value: a list where the first item is the frequency and the second item is a list of positions
            [frequency, [position]] where position is the position in the text where the token is found
    """
    frequencies = dict()
    token_pos = 0

    for token in tokens:
        if token in frequencies:
            frequencies[token][0] += 1
        else: # token does not exist
            frequencies[token] = [1, list()] # set token count equal to 1
        frequencies[token][1].append(token_pos)
        token_pos += 1
    
    return frequencies

def compute_token_frequencies2(tokens):
    """Computes the frequency of tokens
    
    Parameters
    ----------
    tokens : list
        list of tokens 
    
    Returns
    -------
    dict
        a dictionary containing a token: count key-value pair
    
    """
    frequencies = dict()
    
    for token in tokens:
        if token in frequencies:
            frequencies[token] += 1
        else: # token does not exist
            frequencies[token] = 1 # set token count equal to 1
    
    return frequencies

if __name__ == "__main__":
    sample = '''In the heart of the ancient forest, where the canopy was so thick that sunlight barely touched the ground, lived a girl named Elara. 
    She had grown up among the towering trees and whispering leaves, her only companions the creatures of the wood and the distant echo of her mother's 
    lullabies. One evening, as the sky blazed with the colors of dusk, Elara stumbled upon a hidden glade. In its center stood a tree unlike any other, 
    its bark shimmering with an ethereal glow. Intrigued, she approached and found a small, intricately carved box nestled among its roots. As she opened it, 
    a soft, golden light enveloped her, and she heard a voice, gentle yet commanding, You have been chosen, Elara, to awaken the ancient guardians and restore 
    balance to our world. Thus began her journey, one that would take her far beyond the familiar confines of her forest home and into realms of magic and 
    danger she had never imagined. danger she. never imagined.'''

    tokens = parse_document(sample)
    print(tokens)

    # freqMap1 = compute_token_frequencies(tokens)
    # freqMap2 = compute_token_frequencies2(tokens)

    # for key, val in freqMap1.items():
    #     print(f"{key}: {val}")

    # for key, val in freqMap2.items():
    #     print(f"{key}: {val}")
 
