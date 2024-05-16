import chromadb

class ChromaDB:
    def __init__(self):
        self.chroma_client = chromadb.PersistentClient(path="./data/main")
        self.collection = self.chroma_client.get_or_create_collection(
            name="main_collection",
            metadata={"hnsw:space": "cosine"}
        )

    def add(self, documents):
        count = self.collection.count()
        ids = 'id' + str(count + 1)
        print(ids)
        self.collection.upsert(
            documents=documents,
            ids=ids, 
        )

        return self.selectById(ids)
    
    def selectById(self, ids):
        result = self.collection.get(
            ids=[ids]
        )
        return result
    
    def search(self, text, limit):
        results = self.collection.query(
            query_texts=[text], # Chroma will embed this for you
            n_results=limit, # how many results to return
        )
        return results