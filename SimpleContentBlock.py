from bs4 import BeautifulSoup
import requests
import re

def FindSimpleContentBlock(htmlContent : bytes, threshold : float = .5, lineBreak : int = 15) -> list | str:
    """Find content blocks of given the html content.
    
    Parameters
    ----------
    htmlContent : bytes
        bytes representing the all of the html content
    threshold : float
        a float number that is used to determine whether or not a block should be considered
    lineBreak : int
        an integer representing the number of characters that are on a line before a new line occurs (words will not be truncated)
    
    Returns
    -------
    list
        a list of all content blocks
    str
        a formatted string output of the content
    """

    #Variables used in multiple parts of the function
    blocks = list()
    result = list()
    max = 0

    # Find paragraphs within website
    soup = BeautifulSoup(htmlContent, 'html.parser')
    paragraphs = soup.find_all("p")

    for paragraph in paragraphs:
        blocks.append(paragraph.text)
        tokenSize = len(paragraph.text.split())
        if tokenSize > max:
            max = tokenSize

    # Determine which paragraphs are important based on a threshold
    pattern = "[\r\t\n ]{2,}"

    for block in blocks:
        if len(block.split()) >= threshold * max:
            content = block.strip()
            content = " ".join(re.split(pattern, content))
            result.append(content)
    
    # Output to file and write to multiline string output
    stringOutput = "\n".join(result) # One line string output
    formattedOutput = "" # Multiline string output

    with open("temp.txt", "w+") as f:
        index = 0
        for contentBlock in stringOutput.split("\n"):
            count = 0
            #Output individual words
            for word in contentBlock.split():
                f.write(word + " ")
                formattedOutput += word + " "
                if count > lineBreak:
                    f.write("\n")
                    formattedOutput += "\n"
                    count = 0
                count += len(word) + 1
            
            # Separate paragraphs with newlines
            if index < len(result)-1:
                f.write("\n")
                formattedOutput += "\n"
                if formattedOutput[-2] != "\n":
                    f.write("\n")
                    formattedOutput += "\n"
            index += 1

    return result, formattedOutput


if __name__ == "__main__":
    resp = requests.get("https://en.wikipedia.org/wiki/Natural_language_processing")
    result, output = FindSimpleContentBlock(resp.content, .8, 120)
    print(output)