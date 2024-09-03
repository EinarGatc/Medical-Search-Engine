from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import requests
import query
import llm
from parse import parse_document
from bs4 import BeautifulSoup
f1 = open(query.filepath1)

app = Flask(__name__,template_folder='../')
CORS(app)
@app.route('/api/urls', methods=["POST"])
@cross_origin()
def RetrieveRelevantUrls():
    """Find urls that match the query requested.
    
    Parameters
    ----------
    query: str
        a string that will be used to retreive relevant urls passed through POST method
    
    Returns
    -------
    json: dict
        a dictionary/json that contains the requested query and the urls associated with it
    """
    data = request.get_json()
    field = data["query"]
    urls = query.find_query(field,f1)
    return jsonify({'query':field,'urls':urls})

@app.route('/api/cache', methods=["POST"])
def UpdateCache():
    """Updates the cache and clear query postings
    
    Parameters
    ----------
    None
    
    Returns
    -------
    None
    """

    for k, v in query.query_postings.items():
        query.query_cache.put(k, v)
    query.query_postings.clear()
    return jsonify({})

@app.route('/api/content', methods=["POST", "GET"])
def GetHTMLContent():
    data = request.get_json()

    try:
        page = requests.get(data['url'],timeout=1)
        text = page.content.decode(page.encoding)
        text = BeautifulSoup(text, "html.parser")
        text = parse_document(text.get_text().strip().lower())
        return jsonify({'summary':llm.Summarize(text)})
    except:
        return jsonify({'summary':"Failed To Get Summary"})

@app.route('/api/query', methods=["POST"])
def AIOverview():
    data = request.get_json()
    field = data["query"]
    try:
        return jsonify({'overview':llm.Query(field)})
    except:
        return jsonify({'overview':"AI Overview not available"})


if __name__ == "__main__":
    app.run(debug=True)