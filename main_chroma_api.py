from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import chromadb
import os


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

chroma_client = chromadb.PersistentClient(path="./data/main")

collection = chroma_client.get_or_create_collection(
    name="my_collection",
    metadata={"hnsw:space": "cosine"} 
)
#insert documents in chromadb
@app.route('/api/v1/add', methods=['POST'])
def insert_data():
    documents = request.json.get('documents')

    if not documents:
        return jsonify({'error': 'No documents provided'}), 400

    count = collection.count()
    
    collection.upsert(
            documents=[documents],
            ids='id' + str(count+1),
        )
    return jsonify({'message': 'Documents added successfully'}), 200

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

    results = collection.query(
        query_texts=[text], # Chroma will embed this for you
        n_results=limit, # how many results to return
    )

    return jsonify(results['documents']), 200


@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug = True) 