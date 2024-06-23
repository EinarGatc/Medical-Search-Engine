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

#     with open(filePath, 'r', encoding='utf-8') as file:
#         buffer = file.read(bufferSize)
#         while buffer:
#             tokens.append(pattern.findall(buffer))
#             buffer = file.read(bufferSize)
        
#     return tokens

def tokenize(filePath):
    pattern = re.compile(r"\b\w+(?:'\w+)?\b")
    tokens = []

    with open(filePath, 'r', encoding='utf-8') as file:


def computeTokenFreq(tokensList):
    freqMap = {}
    for token in tokensList:
        if token in freqMap:
            freqMap[token] += 1
        else:
            freqMap[token] = 1

    alphabeticalSort = sorted(freqMap.items(), key=lambda x: x[0]) # sort by key
    sortedFreqMap = dict(sorted(alphabeticalSort, key=lambda x: x[1], reverse=True)) # sort by value
    
def printFrequencies(frequencyMap):
    for token, frequency in frequencyMap.items():
        print(f"{token}: {frequency}")

if __name__ == "__main__":
    tokens1 = tokenize('Medical-Search-Engine\RomeoJuliet.txt')
    # tokens1map = computeTokenFreq(tokens1)
    # printFrequencies(tokens1map)
    for tokens in tokens1:
        print(tokens)