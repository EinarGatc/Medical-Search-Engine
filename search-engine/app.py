from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import query

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
    query.query_postings.clear()
    return jsonify({'query':field,'urls':urls})

if __name__ == "__main__":
    app.run(debug=True)