from langchain.vectorstores import Chroma
from langchain.embeddings.huggingface import HuggingFaceEmbeddings

db = Chroma (
    collection_name='123',
    embedding_function=HuggingFaceEmbeddings(model_name="shibing624/text2vec-base-chinese",model_kwargs={"device": "cpu"})
    persist_directory="./data/langchain/main"
)
db.add_documents()