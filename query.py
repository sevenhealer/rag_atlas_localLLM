from sentence_transformers import SentenceTransformer
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

mongodb_uri = os.getenv("MONGO_URI")
client = MongoClient(mongodb_uri)
db = client['rag']
rag_v0 = db['rag_v0']

model = SentenceTransformer('all-miniLM-L6-v2')

query = "what is deepseek?"

query_embedding = model.encode([query], convert_to_numpy=True)[0].tolist()

pipeline = [
    {
        '$vectorSearch': {
            'index': 'rag_search',
            'path': 'embedding',
            'queryVector': query_embedding,
            'numCandidates': 384,
            'limit': 3
        }
    }, {
    '$project': {
      '_id': 0, 
      'text': 1, 
      'score': {
        '$meta': 'vectorSearchScore'
      }
    }
  }
]

results = list(rag_v0.aggregate(pipeline))

print(results)
