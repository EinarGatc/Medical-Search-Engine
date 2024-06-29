import re

stopwordsList = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", 
                 "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", 
                 "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", 
                 "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", 
                 "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", 
                 "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", 
                 "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", 
                 "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]

def Tokenize(text):
  """Gather all the tokens from a text string. Tokens must not be stopwords, single numbers, or single letters.
    
    Parameters
    ----------
    text : string
        a string of HTML content
    
    Returns
    -------
    list
        a list of tokens
  """

  pattern = re.compile(r"\b[A-Za-z0-9]+(?:'[A-Za-z0-9]+)?\b")
  tokens = pattern.findall(text.lower())

  filteredTokens = []
  for token in tokens:
      if token not in stopwordsList and len(token) > 1:
          filteredTokens.append(token)

  return filteredTokens

def ComputeTokenFreq(tokensList):
  """Counts the number of occurences of each token in a list of tokens
    
    Parameters
    ----------
    tokensList : list
        a list of tokens
    
    Returns
    -------
    freqMap : dictionary
        a dictionary of tokens and their counts {token: frequency}
  """

  freqMap = {}
  for token in tokensList:
      if token in freqMap:
          freqMap[token] += 1
      else:
          freqMap[token] = 1

  alphabeticalSort = sorted(freqMap.items(), key=lambda x: x[0]) # sort by key
  sortedFreqMap = dict(sorted(alphabeticalSort, key=lambda x: x[1], reverse=True)) # sort by value

  return sortedFreqMap
    

def PrintFrequencies(frequencyMap):
    """Iterates through a dictionary of tokens mapped to their frequency and prints each token and its frequency
    
    Parameters
    ----------
    freqMap : dictionary
        a dictionary of tokens and their counts {token: frequency}
    
    Returns
    -------
    token: frequency 
        for each token in the dictionary
  """
  for token, frequency in frequencyMap.items():
      print(f"{token}: {frequency}")

def TokenizeUnitTesting():
    assert Tokenize("! @ &*") == []
    assert Tokenize("$7$") == []
    assert Tokenize("don't") == ["don't"]
    assert Tokenize("") == []
    assert Tokenize("class classes'") == ["class", "classes"]
    assert Tokenize("~``` husband") == ["husband"]
    assert Tokenize("") == []
    assert Tokenize("editor-in-chief") == ["editor", "chief"]
    print("Passed Tokenize Unit Testing")

if __name__ == "__main__":
  # Testing Tokenizer for html format of medlineplus.gov
  TokenizeUnitTesting()