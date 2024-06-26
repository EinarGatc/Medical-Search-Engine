import re

# tokenize one document
#filePath = 'testFile.txt'

stopwordsList = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", 
                 "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", 
                 "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", 
                 "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", 
                 "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", 
                 "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", 
                 "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", 
                 "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]


# def tokenize(filePath, bufferSize=1024):
#     pattern = re.compile(r"\b\w+(?:'\w+)?\b")
#     tokens = []
#     partial_token = ''

#     with open(filePath, 'r', encoding='utf-8') as file:
#         while True:
#             buffer = file.read(bufferSize)
#             if not buffer:
#                 break

#             buffer = partial_token + buffer.lower()
#             found_tokens = pattern.findall(buffer)
            
#             # if the buffer ends with an alphanumeric character, the last token might be incomplete
#             if buffer[-1].isalnum():
#                 partial_token = found_tokens.pop() if found_tokens else ''
#             else:
#                 partial_token = ''
            
#             tokens.extend(found_tokens)
    
#     if partial_token:
#         tokens.append(partial_token)

#     return tokens

def tokenize(content):
    pattern = re.compile(r"\b\w+(?:'\w+)?\b")
    
    tokens = []
    tokens = pattern.findall(content)

    filteredTokens = []
    for token in tokens:
        if token not in stopwordsList and len(token) > 1:
            filteredTokens.append(token)

    return filteredTokens

def computeTokenFreq(tokensList):
    freqMap = {}
    for token in tokensList:
        if token in freqMap:
            freqMap[token] += 1
        else:
            freqMap[token] = 1

    alphabeticalSort = sorted(freqMap.items(), key=lambda x: x[0]) # sort by key
    sortedFreqMap = dict(sorted(alphabeticalSort, key=lambda x: x[1], reverse=True)) # sort by value

    return sortedFreqMap
    

def printFrequencies(frequencyMap):
    for token, frequency in frequencyMap.items():
        print(f"{token}: {frequency}")


if __name__ == "__main__":
    # Testing
    tokens1 = tokenize('Medical-Search-Engine\RomeoJuliet.txt')
    tokens1map = computeTokenFreq(tokens1)
    printFrequencies(tokens1map)
