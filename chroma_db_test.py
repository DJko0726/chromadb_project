import chromadb

chroma_client = chromadb.PersistentClient(path="./data")
# switch `create_collection` to `get_or_create_collection` to avoid creating a new collection every time
collection = chroma_client.get_or_create_collection(
    name="my_collection",
    metadata={"hnsw:space": "ip"} 
)

# switch `add` to `upsert` to avoid adding the same documents every time
collection.upsert(
    documents=[
        "pen pineapple apple pen",
        "This is a document about oranges",
        "This is not a computer"
    ],
    ids=["id1", "id2","id3"]
)

results = collection.query(
    query_texts=["This is a query document about florida"], # Chroma will embed this for you
    n_results=5, # how many results to return
    # where={"metadata_field": "pineapple"}
    # where_document={"$contains":"grape"}
)
# collection.peek() # returns a list of the first 10 items in the collection
# collection.count() # returns the number of items in the collection
# collection.modify(name="new_name") # Rename the collection