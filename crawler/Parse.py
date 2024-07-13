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

  return freqMap
    

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

def printFrequencies(frequencyMap):
  for token, frequency in frequencyMap.items():
      print(f"{token}: {frequency}")

def TokenFrequencyTest1():
  tokens = ["this","is","a","sample","token"]
  assert(ComputeTokenFreq(tokens) == {"this":1,"is":1,"a":1,"sample":1,"token":1})

def TokenFrequencyTest2():
  tokens = []
  assert(ComputeTokenFreq(tokens) == {})

def TokenFrequencyTest3():
  tokens = ["a","bear","in","a","barn"]
  assert(ComputeTokenFreq(tokens) == {"a":2,"bear":1,"in":1,"barn":1})

def TokenFrequencyTest4():
  tokens = ["1","2","3","4","5","10","01"]
  assert(ComputeTokenFreq(tokens) == {"1":1,"2":1,"3":1,"4":1,"5":1,"10":1,"01":1})

def TokenFrequencyTest5():
  tokens = ["A","a","wsx","wsx"]
  assert(ComputeTokenFreq(tokens) == {"A":1,"a":1,"wsx":2})

if __name__ == "__main__":
  # Testing Tokenizer for html format of medlineplus.gov
  TokenizeUnitTesting()
  TokenFrequencyTest1()
  TokenFrequencyTest2()
  TokenFrequencyTest3()
  TokenFrequencyTest4()
  TokenFrequencyTest5()