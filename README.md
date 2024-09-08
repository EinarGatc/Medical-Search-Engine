# HealthPro Search Engine

https://github.com/user-attachments/assets/ed7c8123-8d2e-4909-994f-ae7466652201

## Description

HealthPro Search Engine is a web-based platform that enables users to search for information related to various diseases, such as diabetes, cardiovascular diseases, respiratory infections, and more. The platform provides relevant links from trusted domains that have been crawled in advance, offering accessible health information. The backend integrates Meta's Llama 3.1 LLM to generate summaries for each result, enhancing user experience by providing concise and informative content. The frontend is powered by a responsive design using React.js.

## Features

- Search for health-related information on diseases like:
  - Diabetes
  - Cardiovascular diseases
  - COVID-19
  - Common cold
  - Respiratory diseases
  - Influenza
- Retrieve links from trusted medical websites such as with AI generated summaries:
  - [medlineplus.gov](https://medlineplus.gov)
  - [ncbi.nlm.nih.gov](https://ncbi.nlm.nih.gov)
  - [cdc.gov](https://cdc.gov)
  - [mayoclinic.org](https://mayoclinic.org/patient-care-and-health-information)
  - [merckmanuals.com](https://merckmanuals.com/home)
  - [nnlm.gov](https://nnlm.gov/guides)
  - [ahrq.gov](https://ahrq.gov)

## Technologies Used

- **Frontend:** HTML, CSS, JavaScript, React.js
- **Backend:** Python, Flask
- **Libraries:** BeautifulSoupl, RegEx, nltk
- **API Integration:** Llama 3.1 (Meta's LLM)

## Key Components

- **Web Crawler:**   
Utilizes techniques like sim hashing, chunking, text preprocessing, stemming, and indexing to acquire and process web data. This ensures that the content is transformed into a searchable format, while detecting and avoiding near-duplicate content. Over 9000+ documents are crawled and saved to the index during this process.

- **Storage:**  
Data is stored locally using a combination of URL, content type, and encoding (UTF-8). Pickling and batching techniques are used to optimize data storage and retrieval processes, allowing efficient management of large data.

- **Search Engine:**  
Implements advanced filtering based on user queries to return the most relevant documents from the crawled domains. It manages near-duplicates, avoids traps, and incorporates PageRank algorithms to rank results. Additionally, the search engine uses TF-IDF (Term Frequency-Inverse Document Frequency) for relevance scoring and supports bigram and trigram indexing to enhance the search accuracy. Threading is also utilized to maintain quick query response times, ensuring they stay below 300 ms.

- **Llama 3.1 Integration:**  
For each search result, Meta's Llama 3.1 LLM generates a general summary of the search term, along with a detailed summary for each link upon request. This provides users with a quick and concise overview of the content, helping them assess the relevance of the information to their query efficiently.

## Development Breakdown

Detailed breakdown of tasks and functionalities (Not Updated):
[Development Tracker](https://docs.google.com/spreadsheets/d/1vsqg4zMGd2XRCh5tZpoT_6qzItl3ja7oGtht_uOl1sw/edit?usp=sharing)

## License

This project is licensed under the [MIT License](LICENSE).

© Einar Gatchalian, Jason Nguyen, Hearty Parrenas 2024. All Rights Reserved.
