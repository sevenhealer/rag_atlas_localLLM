from sentence_transformers import SentenceTransformer
from pymongo import MongoClient
from dotenv import load_dotenv
from transformers import pipeline
import gradio as gr
import os

load_dotenv()

mongodb_uri = os.getenv("MONGO_URI")
client = MongoClient(mongodb_uri)
db = client['rag']
rag_v0 = db['rag_v0']

embedding_model = SentenceTransformer('all-miniLM-L6-v2')
generate_model = pipeline("text2text-generation", model="google/flan-t5-small")

def get_answer_from_query(user_query):
    query_embedding = embedding_model.encode([user_query], convert_to_numpy=True)[0].tolist()

    query_pipeline = [
        {
            '$vectorSearch': {
                'index': 'rag_search',
                'path': 'embedding',
                'queryVector': query_embedding,
                'numCandidates': 384,
                'limit': 3
            }
        }, 
        {
            '$project': {
                '_id': 0, 
                'text': 1, 
                'score': {
                    '$meta': 'vectorSearchScore'
                }
            }
        }
    ]

    results = list(rag_v0.aggregate(query_pipeline))
    chunks = [result['text'] for result in results]

    retrieved_context = " ".join(chunks)

    query_hf_input = f"Context: {retrieved_context}\n\nQuestion: {user_query}\n\nAnswer:"
    answer = generate_model(query_hf_input, max_length=200, do_sample=True)

    generated_answer = answer[0]['generated_text']

    return chunks, generated_answer

def gradio_interface(query):
    chunks, answer = get_answer_from_query(query)
    return f"**Relevant Chunks:**\n\n{'\n\n'.join(chunks)}", f"**Generated Answer:** {answer}"

interface = gr.Interface(
    fn=gradio_interface,
    inputs=gr.Textbox(lines=2, placeholder="Enter your query here...", label="Query"),
    outputs=[
        gr.Textbox(label="Retrieved Chunks", lines=10),
        gr.Textbox(label="Generated Answer", lines=4)
    ],
    title="RAG with MongoDB and LLM",
    description="Ask a question, and this system will retrieve relevant information from MongoDB and generate an answer using a pretrained LLM."
)

interface.launch(server_name="0.0.0.0", server_port=7860)