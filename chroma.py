import chromadb

class ChromaDB:
    def __init__(self):
        self.chroma_client = chromadb.PersistentClient(path="./data/main")
        self.collection = self.chroma_client.get_or_create_collection(
            name="main_collection",
            metadata={"hnsw:space": "cosine"}
        )

    def add(self, documents):
        try:
            count = self.collection.count()
            doc_ids = 'id' + str(count + 1)
            
            self.collection.upsert(
                documents=documents,
                ids=doc_ids,
            )
            
            return self.select_by_id(doc_ids)
        except Exception as e:
            print(f"Error while adding documents: {e}")
            return None

    def select_by_id(self, ids):
        try:
            result = self.collection.get(
                ids=[ids]
            )
            return result
        except Exception as e:
            print(f"Error while selecting by ID: {e}")
            return None

    def search(self, text, limit=10):
        try:
            results = self.collection.query(
                query_texts=[text], 
                n_results=limit
            )
            return results
        except Exception as e:
            print(f"Error while searching: {e}")
            return None
