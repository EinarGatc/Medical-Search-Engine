from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

model = OllamaLLM(model="llama3.1")

def Query(text):
    prompt = ChatPromptTemplate([
        (
            "system",
            "You are search engine assistant that provides information regarding health. Provide the definition of the disease, symptoms of the disease, and treatments for the disease. It is important that your clarify that your answer is just a recommendation. Do not ask for any clarifications. Provide a clear break for each section, so that the text can be parsed easily."
        ),
        ("human", "{query}"),
    ])
    chain = prompt | model
    return chain.invoke({"query":text})

def Summarize(text):
    prompt = ChatPromptTemplate([
        (
            "system",
            "You are a document assistant that summarizes documents into their main points. Introduce the topic, discuss the main points, provide supporting arguments within the document, and conclude with a final point.Do not ask for any clarifications. Provide a clear break for each section, so that the text can be parsed easily."
        ),
        ("human", "{document}"),
    ])
    chain = prompt | model
    return chain.invoke({"document": text})

if __name__ == "__main__":
    text = input("Query: ")
    while text:
        print(Query(text))
        text = input("Query: ")
    
