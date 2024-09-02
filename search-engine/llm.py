from langchain_ollama import OllamaLLM

model = OllamaLLM(model="llama3")
model.invoke(input="Your role is to teach users information regarding diseases. You will be given both questions to answer and documents to summarize. It is important to know that this should just be a recommendation.")

def Query(text):
    prompt = f"I am giving you a query. Provide information on the query. Provide the definition of the disease, symptoms of the disease, and treatments for the disease. Query: {text}"
    return model.invoke(input=prompt)

def Summarize(text):
    prompt = f"You are being given a document. Summarize the document's content. Document Content: {text}"
    return model.invoke(input=prompt)

if __name__ == "__main__":
    text = input("Query: ")
    while text:
        print(Query(text))
        text = input("Query: ")
