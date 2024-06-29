from bs4 import BeautifulSoup
from parse import tokenize
import requests
import matplotlib.pyplot as plt
import numpy as np
import math
"""
    
    Parameters
    ----------
    
    Returns
    -------
    
    """
def FindContentBlock(htmlContent:bytes, consecutiveChunks:int=3) -> list[str]:
    """Find intervals of content within the html.
    
    Parameters
    ----------
    htmlContent : bytes
        a byte representation of the html content
    consecutiveChunks : int
        an integer representing the number of consecutive chunks to start with
    
    Returns
    -------
    list[str]
        a list of tokens that contains text only within important intervals

    """

    prevIntervals = None
    dsc = CreateDSC(htmlContent)
    slope, intercept = CalculateSlopeDSC(dsc)
    windowSize = ActivationFunction(len(dsc))
    # VisualizeDSC(dsc, slope, intercept)
    
    slopesLow, totalLowTokens = DetermineLowSlopeSections(dsc, windowSize, slope, consecutiveChunks)
    while totalLowTokens > len(dsc) * .1 and sum([value[1] for value in slopesLow]) / len(slopesLow) <= .5 * slope:
        prevIntervals = slopesLow
        consecutiveChunks += 1
        slopesLow, totalLowTokens = DetermineLowSlopeSections(dsc, windowSize, slope, consecutiveChunks)
    
    # print(sum([value[1] for value in slopesLow]) / len(slopesLow), .5 * slope)
    
    joinedIntervals = JoinIntervals(prevIntervals)
    return GetContentOfIntervals(htmlContent, joinedIntervals)

def JoinIntervals(slopesLow:list[list[tuple[int,int],int]]) -> list[tuple[int,int]]:
    """Joins intervals together
    
    Parameters
    ----------
    slopesLow : list[list[tuple[int,int],int]]
        list of intervals and their corresponding line of best fit slopes

    Returns
    -------
        list[tuple[int,int]]
            list of joined intervals
    
    """

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

    if prev:
        result.append(prev)

    return result



def DetermineLowSlopeSections(dsc:list[tuple[int,int]], windowSize:int, slopeDSC:int, consecutiveChunks:int) -> list[list[tuple[int,int], int]]:
    """Determine low slope section of the dsc graph
    
    Parameters
    ----------
    dsc : list[tuple[int,int]]
        document slope curve graph
    windowSize : int
        size of each chunk
    slopeDSC : int
        slope of line of best fit
    consecutiveChunks : int
        number of needed consecutive chunks

    Returns
    -------
    list[list[tuple[int,int], int]]
        list of important intervals and their corresponding slopes

    """

    result = list()
    totalTokens = len(dsc)
    totalChunks = 2 * math.ceil(totalTokens/windowSize)
    lowFlag = False
    chunks = []
    slopes = []
    prevSlopes = [None] * (consecutiveChunks-1)
    totalLowTokens = 0

    for i in range(totalChunks-consecutiveChunks):
        chunks = [((i+j)*windowSize//2, (i+j+1)*windowSize//2) if (i+j+1)*windowSize//2 <= totalTokens  else ((i+j)*windowSize//2, totalTokens) for j in range(consecutiveChunks)]
        slopes = [prevSlopes[j] if j != consecutiveChunks-1 and prevSlopes[j] else CalculateSlopeDSC(dsc[chunk[0]:chunk[1]])[0] for j, chunk in enumerate(chunks)]
        print(chunks)
        prevSlopes.clear()
        prevSlopes = [slopes[j+1] for j in range(consecutiveChunks-1)]

        if all(slope > slopeDSC * .5 for slope in slopes):
            lowFlag = False
        elif all(slope <= slopeDSC * .5 for slope in slopes):
            result.append([chunks[0], slopes[0]])
            totalLowTokens += chunks[0][1] - chunks[1][0] + 1
            lowFlag = True
        elif lowFlag:
            result.append([chunks[0], slopes[0]])
            totalLowTokens += chunks[0][1] - chunks[0][0] + 1
        
    if lowFlag:
        [result.append([chunks[i+1], prevSlopes[i]]) for i in range(len(prevSlopes))]
        totalLowTokens += sum([chunks[i][1] - chunks[i][0] + 1 for i in range(1, len(chunks))])
    
    return result, totalLowTokens

        


def CalculateSlopeDSC(dsc:list[int,int]) -> int | int:
    """Calculate the average slope of the dsc graph
    
    Parameters
    ----------
    dsc : list[int,int]
        document slope curve graph

    Returns
    -------
    int
        slope of the line of best fit
    int
        y-intercept of the line of best fit
    """
    #Account for cases where there are a small number of points
    x_values, y_values = zip(*dsc)


    # Perform least squares regression
    # Convert lists to numpy arrays for easier computation
    x_values = np.array(x_values)
    y_values = np.array(y_values)

    # Calculate coefficients (slope and intercept) using numpy's polyfit function
    slope, intercept = np.polyfit(x_values, y_values, 1)

    return slope, intercept

def VisualizeDSC(dsc:list[tuple[int,int]], slope:int, intercept:int) -> None:
    """ Visualize the dsc graph and the line of best fit
    
    Parameters
    ----------
    dsc : list[tuple[int,int]]
        document slope curve graph
    slope : int
        slope of the line of best fit
    intercept : int
        y-intercept of the line of best fit

    Returns
    -------
    None
    """

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

def ActivationFunction(tokenCount:int, minWindowSize:int=8, maxWindowSize:int=50, lower:int=200, upper:int=5000) -> int:
    """Determine the number of tokens within each chunk
    
    Parameters
    ----------
    tokenCount : int
        total number of tokens
    minWindowSize : int
        minimum window size 
    maxWindowSize : int
        maximum window size 
    lower : int
        minimum number of tokens
    upper : int
        maximum number of tokens

    Returns
    -------
    int
        number of tokens within each chunk

    """

    if tokenCount <= lower:
        return minWindowSize
    elif tokenCount >= upper:
        return maxWindowSize
    else:
        return minWindowSize + int(((maxWindowSize-minWindowSize) / (upper - lower)) * (tokenCount-lower))
    
def CreateDSC(htmlContent:bytes) -> list[tuple[int,int]]:
    """Create the dsc graph
    
    Parameters
    ----------
    htmlContent : bytes
        byte representation of the html content
    
    Returns
    -------
    list[tuple[int,int]]
        dsc graph where the tuple represents each coordinate

    """

    soup = BeautifulSoup(htmlContent, 'html.parser')
    
    totalTags, totalTokens = 0, 0 
    result = [(0,0)]

    for tag in soup.find_all():
        if tag.get_text().strip():
            tokens = tokenize(tag.get_text().strip().lower())
            # tokens = tag.get_text().strip().lower().split()
            totalTags += 1
            for token in tokens:
                totalTokens += 1
                result.append((totalTokens, totalTags))
    
    return result

def GetContentOfIntervals(htmlContent:bytes, intervals:list[tuple[int,int]]) -> list[str]:
    """Get the text within the specified intervals
    
    Parameters
    ----------
    htmlContent : bytes
        byte representation of the html content
    intervals : list[tuple[int,int]]
        intervals for important text
    
    Returns
    -------
        list[str]
            list of important text
    """

    soup = BeautifulSoup(htmlContent, 'html.parser')
    
    result = []
    count = 0
    pointer = 0

    for tag in soup.find_all():
        if tag.get_text().strip():
            tokens = tokenize(tag.get_text().strip().lower())
            # tokens = tag.get_text().strip().lower().split()
            for token in tokens:
                if pointer >= len(intervals):
                    continue
                if count > intervals[pointer][1]:
                    pointer += 1
                if pointer < len(intervals) and count >= intervals[pointer][0]:
                    result.append(token)
                count += 1
                
    return result

def ActivationFunctionTest1():
    assert(ActivationFunction(10) == 8)

def ActivationFunctionTest2():
    assert(ActivationFunction(7000) == 50)

def ActivationFunctionTest3():
    assert(ActivationFunction(500) == 10)

def JoinIntervalsTest1():
    assert(JoinIntervals([[(1,10),0.1],[(10,11),0.1],[(11,52),0.1],[(53,60),0.1]]) == [(1,52),(53,60)])

def JoinIntervalsTest2():
    assert(JoinIntervals([[(0,1),0.1],[(2,3),0.1],[(4,5),0.1],[(6,7),0.1]]) == [(0,1),(2,3),(4,5),(6,7)])

if __name__ == "__main__":
    # resp = requests.get("https://en.wikipedia.org/wiki/Natural_language_processing")
    #resp = requests.get("https://www.mayoclinic.org/diseases-conditions/abdominal-aortic-aneurysm/symptoms-causes/syc-20350688")

    #tokens = FindContentBlock(resp.content)
    ActivationFunctionTest1()
    ActivationFunctionTest2()
    ActivationFunctionTest3()
    JoinIntervalsTest1()
    JoinIntervalsTest2()
    
    