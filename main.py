from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from chroma import ChromaDB
import os


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)
db = ChromaDB()
#insert documents in chromadb
@app.route('/api/v1/add', methods=['POST'])
def insert_data():
    documents = request.json.get('documents')

    if not documents:
        return jsonify({'error': 'No documents provided'}), 400

    try:
        result = db.add(documents)
        return jsonify({'Data': result}), 200
    except Exception as e:
        return jsonify({'error_message': e}), 200

#search data
@app.route('/api/v1/search',methods=['get'])
def get_data():
    limit = request.args.get('limit', type=int)
    text = request.args.get('text', type=str)

    if not text:
        return jsonify({'error': 'No text provided'}),400
    if limit is not None:
        limit = int(limit)
        if limit < 1:
            return jsonify({'error': 'Limit must be greater than zero'}), 400
    else:
        limit = 10

    result = db.search(text,limit)
    return jsonify(result), 200

#list data
@app.route('/api/v1/list',methods=['get'])
def list_data():
    limit = request.args.get('limit', type=int)

    if limit is not None:
        limit = int(limit)
        if limit < 1:
            return jsonify({'error': 'Limit must be greater than zero'}), 400
    else:
        limit = 10

    results = collection.query(
        limit=limit, # how many results to return
    )

    return jsonify(results), 200


@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug = True) 