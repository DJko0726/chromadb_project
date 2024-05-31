from flask import Flask, request, jsonify, render_template, Response
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from chroma import ChromaDB
from Utility.csv import Csv
from Utility.excel import Excel
from datetime import datetime, timedelta
import logging

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JWT_SECRET_KEY'] = 'DJko_in_the_house' 
CORS(app)
chroma_db = ChromaDB()
jwt = JWTManager(app)

# 日誌設定
logging.basicConfig(level=logging.INFO)

#insert documents in chromadb
@app.route('/api/v1/add', methods=['POST'])
@jwt_required()
def insert_data():
    documents = request.json.get('documents')

    if not documents:
        return jsonify({'error': 'No documents provided'}), 400

    try:
        result = chroma_db.add(documents)
        return jsonify({'Data': result}), 200
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        return jsonify({'error_message': e}), 200

#list data + search sym text
@app.route('/api/v1/list',methods=['get'])
@jwt_required()
def get_data():
    limit = request.args.get('limit',default=10,type=int)
    text = request.args.get('text', type=str)

    if not text:
        return jsonify({'error': 'No text provided'}),400

    try:
        result = chroma_db.search(text, limit)
        if not result['ids']:
            return jsonify({'error': 'must add text first!'}), 200
        return jsonify(result), 200
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        return jsonify({'error_message': str(e)}), 500
    

#download file
@app.route('/api/v1/download',methods=['post'])
@jwt_required()
def download():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    limit = request.json.get('limit',10)
    text = request.json.get('text')
    file_type = request.json.get('file_type', 'csv')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    try:
        result = chroma_db.search(text, limit)
        data = {
            'distances': result['distances'],
            'documents': result['documents'],
            'ids': result['ids'],
            'metadatas': result['metadatas']
        }

        if file_type == 'csv':
            csv_obj = Csv(timestamp)
            return jsonify({'path': csv_obj.download(data)})
        elif file_type == 'excel':
            excel_obj = Excel(timestamp)
            return jsonify({'path': excel_obj.download(data)})
        else:
            return jsonify({'error': 'Invalid file type'}), 400
    except Exception as e:
        logging.error(f"Error downloading file: {e}")
        return jsonify({'error_message': str(e)}), 500

#generate jwt
@app.route('/api/v1/jwt',methods=['post'])
def generateJWT(): 
    username = request.json.get('username')
    password = request.json.get('password')

    if username == 'admin' and password == 'password':
        expires = timedelta(minutes=60)
        access_token = create_access_token(identity=username, expires_delta=expires)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

    

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug = True) 