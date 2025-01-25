from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from pymongo import MongoClient
from dotenv import load_dotenv
import os

with open('./text/sample.txt', 'r') as file:
    data = file.read()

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 50
)
chunks = splitter.split_text(data)

model = SentenceTransformer('all-miniLM-L6-v2')
embeddings = model.encode(chunks)

load_dotenv()

mongodb_uri = os.getenv("MONGO_URI")
client = MongoClient(mongodb_uri)
db = client['rag']
rag_v0 = db['rag_v0']

documents = []
for chunk, embedding in zip(chunks, embeddings):
    document = {
        "text": chunk,
        "embedding": embedding.tolist()
    }
    documents.append(document)

rag_v0.insert_many(documents)