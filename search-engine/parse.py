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
    
    Runtime
    -------
    N is the number of characters in the file
    Create a buffer that reads 1024 bytes from the file and do that for
        the size of the text file O(N)
    Iterate over the buffer and check if a character is alphanumeric O(1)  
    If a character is alphanumeric then add it to the current token
    If a character is non alphanumeric then add the token to the tokens list 
        If the token is not an empty string. Then reset the current working
        token
    If buffer is smaller than the buffer_size (1024), flip the last_line flag
    If the last_line flag is true and the current working token is not
        an empty string, add the token to the tokens list
    Therefore the time complexity of the algorithm is O(N) or in other words 
        linear to the number of characters in the file
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

    # generate bigrams
    textBigrams = list(nltk.bigrams(tokens))
    
    # add bigrams to current list of tokens
    # bigrams are a tuple
    tokens.extend(textBigrams)

    return tokens

def compute_token_frequencies(tokens):
    """Compute the frequency of tokens
    
    Parameters
    ----------
    tokens : list
        list of tokens [(tokens, tag) ... (tokens, tag)]
    
    Returns
    -------
    dict
        a dictionary containing a token (key) and count (value) key-value pair
    
    Runtime
    -------
    n1 is the number of tokens present within the text file, n1 <= N, where N is the number of characters 
        within the text file
    Linear time in the number of tokens within the text file O(n1) = O(N)
        (tokens computed from tokenize function)
    Just iterating over the number of tokens within the text file and adding
        to the token count wihtin the dictionary. 
        If the key exists then add to the token count, which takes O(1) time
        If the key doesnt exist then set the key to the token and set the count to 1 O(1) time
    Therefore the time complexity of the algorithm is O(n1) == O(N) or in other words linear
        to the number of tokens present within the text file, which is at most the number of
        characters, N
    """
    frequencies = dict()
    token_pos = 0
    for token in tokens:

        if isinstance(token, tuple): # if bigram
            if token not in frequencies:
                frequencies[token] = [0, []]
            frequencies[token] = frequencies[token[0]]

        else:
            if token in frequencies:
                frequencies[token][0] += 1
            else: # token does not exist
                frequencies[token] = [1, list()] # set token count equal to 1
            frequencies[token][1].append(token_pos)

        token_pos += 1

    return frequencies

def compute_token_frequencies2(tokens):
    """Compute the frequency of tokens
    
    Parameters
    ----------
    tokens : list
        list of tokens [(tokens, tag) ... (tokens, tag)]
    
    Returns
    -------
    dict
        a dictionary containing a token (key) and count (value) key-value pair
    
    Runtime
    -------
    n1 is the number of tokens present within the text file, n1 <= N, where N is the number of characters 
        within the text file
    Linear time in the number of tokens within the text file O(n1) = O(N)
        (tokens computed from tokenize function)
    Just iterating over the number of tokens within the text file and adding
        to the token count wihtin the dictionary. 
        If the key exists then add to the token count, which takes O(1) time
        If the key doesnt exist then set the key to the token and set the count to 1 O(1) time
    Therefore the time complexity of the algorithm is O(n1) == O(N) or in other words linear
        to the number of tokens present within the text file, which is at most the number of
        characters, N
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
    danger she had never imagined.'''

    tokens = parse_document(sample)
    freqMap1 = compute_token_frequencies(tokens)

    freqMap2 = compute_token_frequencies2(tokens)

    for key, val in freqMap1.items():
        print(f"{key}: {val}")

    for key, val in freqMap2.items():
        print(f"{key}: {val}")
 
