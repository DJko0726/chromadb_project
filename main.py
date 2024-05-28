from flask import Flask, request, jsonify, render_template, Response
from flask_cors import CORS
from chroma import ChromaDB
from Utility.csv import Csv
from Utility.excel import Excel
from datetime import datetime


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)
chroma_db = ChromaDB()

#insert documents in chromadb
@app.route('/api/v1/add', methods=['POST'])
def insert_data():
    documents = request.json.get('documents')

    if not documents:
        return jsonify({'error': 'No documents provided'}), 400

    try:
        result = chroma_db.add(documents)
        return jsonify({'Data': result}), 200
    except Exception as e:
        return jsonify({'error_message': e}), 200

#list data + search sym text
@app.route('/api/v1/list',methods=['get'])
def get_data():
    limit = request.args.get('limit',default=10,type=int)
    text = request.args.get('text', type=str)

    if not text:
        return jsonify({'error': 'No text provided'}),400

    result = chroma_db.search(text,limit)

    if not any(result['ids']):
        return jsonify({'error': 'must add text first!'}), 200
    else:
        return jsonify(result), 200
    

#download file
@app.route('/api/v1/download',methods=['post'])
def download():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    csv_obj = Csv(timestamp)
    excel_obj = Excel(timestamp)

    limit = request.json.get('limit',10)
    text = request.json.get('text')
    file_type = request.json.get('file_type', 'csv')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    result = chroma_db.search(text, limit)
    
    data = {
        'distances': result['distances'],
        'documents': result['documents'],
        'ids': result['ids'],
        'metadatas': result['metadatas']
    }
    
    if file_type == 'csv':
        return jsonify({'path': csv_obj.download(data)})
    elif file_type == 'excel':
        return jsonify({'path': excel_obj.download(data)})

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug = True) 