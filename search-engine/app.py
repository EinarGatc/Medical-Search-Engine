from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import query
import threading
import llm

f1 = open(query.filepath1)

app = Flask(__name__,template_folder='../')
CORS(app)
@app.route('/api/urls', methods=["POST","GET"])
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
    return

if __name__ == "__main__":
    app.run(debug=True)