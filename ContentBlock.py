from bs4 import BeautifulSoup
from parse import tokenize
import requests
import matplotlib.pyplot as plt
import numpy as np
import math

def FindContentBlock(htmlContent) -> str:
    dsc = CreateDSC(htmlContent)
    slope, intercept = CalculateSlopeDSC(dsc)
    windowSize = ActivationFunction(len(dsc))
    # VisualizeDSC(dsc, slope, intercept)
    slopesLow, totalLowTokens = DetermineLowSlopeSections(dsc, windowSize, slope)
    if totalLowTokens > len(dsc) * .1 and sum([value[1] for value in slopesLow]) / len(slopesLow) <= .5 * slope:
        return JoinIntervals(slopesLow)
    
    return None

def JoinIntervals(slopesLow):
    prev = None
    result = []
    for value in slopesLow:
        interval = value[0]
        if prev == None:
            prev = interval
        elif prev[1] == interval[0]:
            prev = (prev[0], interval[1])
        else:
            result.append(prev)
            prev = interval
    result.append(prev)
    return result



def DetermineLowSlopeSections(dsc, windowSize, slopeDSC):
    result = list()
    totalTokens = len(dsc)
    totalChunks = 2 * math.ceil(totalTokens/windowSize)
    lowFlag = False
    prevSlope1 = None
    prevSlope2 = None
    totalLowTokens = 0

    for i in range(totalChunks-3):
        chunk1 = (i*windowSize//2, (i+1)*windowSize//2)
        chunk2 = ((i+1)*windowSize//2, (i+2)*windowSize//2)
        chunk3 = ((i+2)*windowSize//2, totalTokens) if (i+3)*windowSize//2 > totalTokens else ((i+2)*windowSize//2, (i+3)*windowSize//2)

        slope1 = prevSlope1 if prevSlope1 else CalculateSlopeDSC(dsc[chunk1[0]:chunk1[1]])[0]
        slope2 = prevSlope2 if prevSlope2 else CalculateSlopeDSC(dsc[chunk2[0]:chunk2[1]])[0]
        slope3 = CalculateSlopeDSC(dsc[chunk3[0]:chunk3[1]])[0]

        prevSlope1 = slope2
        prevSlope2 = slope3
        if slope1 > slopeDSC * .5 and slope2 > slopeDSC * .5 and slope3 > slopeDSC * .5:
            lowFlag = False
        elif slope1 <= slopeDSC * .5 and slope2 <= slopeDSC * .5 and slope3 <= slopeDSC * .5:
            result.append([chunk1, slope1])
            totalLowTokens += chunk1[1] - chunk1[0] + 1
            lowFlag = True
        elif lowFlag:
            result.append([chunk1, slope1])
            totalLowTokens += chunk1[1] - chunk1[0] + 1
        
    if lowFlag:
        result.append([chunk2, prevSlope1])
        result.append([chunk3, prevSlope2])
        totalLowTokens += chunk2[1] - chunk2[0] + 1
        totalLowTokens += chunk3[1] - chunk3[0] + 1
    
    return result, totalLowTokens

        


def CalculateSlopeDSC(dsc):
    x_values, y_values = zip(*dsc)


    # Perform least squares regression
    # Convert lists to numpy arrays for easier computation
    x_values = np.array(x_values)
    y_values = np.array(y_values)

    # Calculate coefficients (slope and intercept) using numpy's polyfit function
    slope, intercept = np.polyfit(x_values, y_values, 1)

    return slope, intercept

def VisualizeDSC(dsc, slope, intercept) -> None:
    x_values, y_values = zip(*dsc)
    
    x_values = np.array(x_values)
    y_values = np.array(y_values)
    
    predicted_y = slope * x_values + intercept

    # Plot the data points and the linear regression line
    plt.figure(figsize=(8, 6))
    plt.scatter(x_values, y_values, color='blue', label='Data Points')
    plt.plot(x_values, predicted_y, color='red', linestyle='-', label='Linear Regression')
    plt.title('DSC Graph')
    plt.xlabel('Token Count')
    plt.ylabel('Tag Count')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    # Display the plot
    plt.show()

def ActivationFunction(tokenCount, minWindowSize=8, maxWindowSize=50, lower=200, upper=5000) -> int:
    if tokenCount <= lower:
        return minWindowSize
    elif tokenCount >= upper:
        return maxWindowSize
    else:
        return minWindowSize + int(((maxWindowSize-minWindowSize) / (upper - lower)) * (tokenCount-lower))
    
def CreateDSC(htmlContent) -> list:
    soup = BeautifulSoup(htmlContent, 'html.parser')
    
    totalTags, totalTokens = 0, 0 
    result = [(0,0)]

    for tag in soup.find_all():
        if tag.get_text().strip():
            tokens = tokenize(tag.get_text().strip().lower())
            totalTags += 1
            for token in tokens:
                totalTokens += 1
                result.append((totalTokens, totalTags))
    
    return result

def GetContentIntervals(htmlContent, intervals):
    visitedIndex = set()
    soup = BeautifulSoup(htmlContent, 'html.parser')
    
    result = []
    count = 0
    pointer = 0
    with open("temp.txt", "w+") as f:
        for tag in soup.find_all():
            if tag.get_text().strip():
                tokens = tokenize(tag.get_text().strip().lower())
                for token in tokens:
                    if pointer < len(intervals):
                        if count > intervals[pointer][1]:
                            pointer += 1
                        elif count < intervals[pointer][0]:
                            pass
                        else:
                            f.write(token + " ")
                            result.append(token)
                    count += 1
                
    return result

if __name__ == "__main__":
    resp = requests.get("https://www.webmd.com/cancer/cancer-hiring-caregiver")
    intervals = FindContentBlock(resp.content)
    print(GetContentIntervals(resp.content, intervals))
    print(intervals)
    