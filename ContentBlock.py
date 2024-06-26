from bs4 import BeautifulSoup
from Parse import tokenize
import requests

def FindContentBlock(htmlContent) -> str:
    file, count = CreateBitString(htmlContent)
    maxValue = 0
    maxI, maxJ = 1, 2
    print(count)
    for i in range(1, count):
        print(i)
        for j in range(i, count-1):
            print(j)
            file.seek(0, 0)
            total = 0
            for k in range(0, i):
                total += int(file.read(1))
            for k in range(i,j+1):
                total += 1 - int(file.read(1))
            for k in range(j+1, count):
                total += int(file.read(1))
            if total > maxValue:
                maxValue = total
                maxI, maxJ = (i,j)
    print(maxI, maxJ)
    return GetContentBlock(htmlContent, maxI, maxJ)
    

def CreateBitString(htmlContent) -> str | int | int:
    soup = BeautifulSoup(htmlContent, 'html.parser')
    file = open("BitRepresentation.txt", "w+")
    count = 0
    for tag in soup.find_all():
        if tag.get_text().strip():
            tokens = tokenize(tag.get_text().strip().lower())
            file.write("1")
            count += 1
            for token in tokens:
                file.write("0")
                count += 1
    
    return file, count

def GetContentBlock(htmlContent, i, j):
    soup = BeautifulSoup(htmlContent, 'html.parser')
    result = ""
    count = 0

    for tag in soup.find_all():
        if tag.get_text().strip():
            count += 1
            tokens = tokenize(tag.get_text().strip().lower())
            print(tokens)
            for token in tokens:
                if count > j:
                    return result
                if count >= i:
                    result += token + " " 
                count += 1

    return result


if __name__ == "__main__":
    resp = requests.get("https://en.wikipedia.org/wiki/Natural_language_processing")
    print(FindContentBlock(resp.content))