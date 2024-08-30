from bs4 import BeautifulSoup
import json
from parse import parse_document
import re
import stemming

def get_text_from_json(json_file) -> str:
    '''Reads file passed in and returns its content in HTML form.'''
    with open(json_file, 'rb') as file:
        json_data = json.load(file)
    return json_data

def get_token_count(list) -> dict:
    '''Count the unique tokens in a given list and return as a dict.'''
    important_text_dict = dict()
    for token in list:
        if token in important_text_dict:
            important_text_dict[token] += 1
        else:
            important_text_dict[token] = 1
    return important_text_dict
        

def get_tokens_with_tags(element):
    '''Gathers all tokens inside of a tag from the content passed in.'''
    result = dict()
    stemmedToken = []
    
    for tag in element.find_all(["title", "header", "h1", "h2", "h3", "h4", "h5", "h6", "strong", "b",]):
        if tag.get_text().strip():
            tokenList = parse_document(tag.get_text().strip().lower())
            for tokenString in tokenList:
                for token in tokenString.split(" "):
                    stemmedToken.append(stemming.stem_token(token))
                
                newToken = " ".join(stemmedToken)
                if newToken not in result:
                    result[newToken] = set()
                
                result[newToken].add(tag.name)
                stemmedToken.clear()

        # if tag.get_text().strip():
        #     tokens = parse_document(tag.get_text().strip().lower())
        #     for token in tokens:
        #         token = stemming.stem_token(token)
        #         if token not in result:
        #             result[token] = set()
        #         result[token].add(tag.name)
                
    return result

def get_tokens_without_tags(element):
    '''Returns all token not in a tag, as a list, from the content passed in. '''
    result = []
    
    if element.get_text().strip():
        tokenList = parse_document(element.get_text().strip().lower())
        stemmedToken = []
        for tokenString in tokenList:
            for token in tokenString.split(" "):
                stemmedToken.append(stemming.stem_token(token))
            result.append(" ".join(stemmedToken))
            stemmedToken.clear()

    return result

def print_tokens_and_tags(token_tags) -> None:
    '''Prints each token and their tag(s).'''
    for token,tag in token_tags:
        print("Token: '{}' | Tag: '{}'".format(token,tag))


# def get_important_text(text) -> list: 

#     important_content = []

#     # Find all tags you're interested in
#     nested_tags = text.find_all(["div", "p", "li", "ul", "span", "section"], recursive=True)

#     # Find strong tags within the nested tags
#     strong_tags = []
#     for tag in nested_tags:
#         x = tag.find_all(["strong", "b", "title", "h1", "h2", "h3", "h4", "h5", "h6"])
#         if x.get().find_all(["strong", "b", "title", "h1", "h2", "h3", "h4", "h5", "h6"]):
#             print(x)
#             # strong_tags.extend(x.text.strip())  # Focus on strong and bold tags

#     print("Nested Tags: ", len(nested_tags))
#     print("Strong Tags: ", len(strong_tags))

#     # # Extract and print text from strong tags
#     # for x in strong_tags: 
#     #     if x:
#     #         important_content.append(x.text.strip())  # Add stripped text to results
#     print(strong_tags)
#     return important_content



    # for x in nested_tags and strong_tags:
    #     if x:
    #         print(x)


    # for tag in strong_tags:
    #     if tag.text:
    #         # for tag in soup.find_all(["strong", "b", "h1", "h2", "h3", "h4", "h5", "h6"]):
    #         print(soup)
    #         print(tag.text)
    #         text = tag.strip()
    #         important_content.append(text)

    # ======================= strat finding the bold only =============
    # soup = BeautifulSoup(data["content"], "html.parser")
    # # nested_tags = soup.find_all(["div", "p", "li", "ul", "span", "section"])
    # tags = soup.find_all(["strong", "b", "h1", "h2", "h3", "h4", "h5", "h6", "title"])
    # for tag in tags:
    #     if tag:
    # # # for tag in soup.find_all(["strong", "b", "h1", "h2", "h3", "h4", "h5", "h6"]):
    #         text = tag.text.strip()
    #         print(text)
    #         important_content.append(tag)

    # return important_content

if __name__ == "__main__":
    random_json_file = "/Users/shika/Downloads/DEV/aiclub_ics_uci_edu/8ef6d99d9f9264fc84514cdd2e680d35843785310331e1db4bbd06dd2b8eda9b.json"
    # random_json_file = "/Users/shika/Assignment3/DEV/scale_ics_uci_edu/4af1a3348e0a5837673376a91138a73cc3f01798a1f46ae90f21bc8c9bd77df1.json"
    # random_json_file = "/Users/shika/Assignment3/DEV/aiclub_ics_uci_edu/9a59f63e6facdc3e5fe5aa105c603b545d4145769a107b4dc388312a85cf76d5.json"
    # random_json_file = "/Users/shika/Assignment3/DEV/scale_ics_uci_edu/71be70831646eb8637d7eb70a785b174b7d042fa85248e30bbd8f33404673ff1.json" # no class on the strong tag
    # tags = get_text_from_json(random_json_file)
    # text_list = tags.find('strong')
    # # text_list = get_important_text(tags)
    # print(text_list)
    # # for elem in text_list:
    #     if elem:
    #         print(elem)

    # parent_tag = text.find('b', class_=True)

    # if parent_tag:
    #     # Find all nested tags within the parent tag
    #     nested_tags = parent_tag.find_all(recursive=True)
        
    #     # Print the nested tags
    #     for tag in nested_tags:
    #         print(tag)
    # else:
    #     print("Parent tag not found.")

    # print(text.find_all())

    # TESTING FOR GET IMPORTANT TEXT (BOLD, HEADERS, TITLE, ETC...)
    # print(text)
    # test = get_important_text(text)
    # print(len(test))
    # print(test)


    # TESTING FOR GET TOKEN WITH TAG
    # tokens_with_tags = list(get_tokens_with_tags(text_list))
    # print(tokens_with_tags)
    # print_tokens_and_tags(tokens_with_tags)


    # TESTING FOR TOKEN COUNT WORKS (still need to split the words in a sentence into tokens)
    # test = ["a", "b", "c", "d", "a", "a", "ap sda"]
    # myDict = get_token_count(test)
    # print(myDict)
