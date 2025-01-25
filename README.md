# RAG (Retriever-augmented Generation) with MongoDB Atlas and Sentence Transformers

This project demonstrates a **Retriever-Augmented Generation (RAG)** approach to building a text-based search engine that can retrieve relevant text chunks from a file and generate answers to user queries using **Sentence Transformers** for embeddings and **MongoDB Atlas** for efficient storage and vector search.

## Overview

- **Upload.py**: Reads a text file, splits it into chunks, generates embeddings for each chunk using **Sentence Transformers**, and stores the chunks and embeddings in **MongoDB Atlas**.
- **Query.py**: Queries the stored embeddings from MongoDB Atlas, retrieves the most similar chunks using **vector search**, and returns the relevant results based on cosine similarity.

---

## Requirements

- Python 3.7+
- MongoDB Atlas account (with a cluster set up for vector search)
- MongoDB URI stored in a `.env` file

---

## Setup

### 1. Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/rag-project.git
cd rag-project
```

### 2. Install Dependencies

Install the necessary Python dependencies using pip:

```bash
pip install -r requirements.txt
```

The required dependencies include:

- sentence-transformers: For generating embeddings.
- pymongo: For connecting to MongoDB Atlas.
- dotenv: For loading environment variables.
- langchain: For text splitting.

### 3. Set Up MongoDB Atlas

Create an Atlas account and set up a cluster if you don't have one.
Create a database (rag) and a collection (rag_v0).
Set up Vector Search in MongoDB Atlas (for more details, check the MongoDB documentation).
Add your MongoDB URI to a .env file:

```bash
MONGO_URI="your_mongodb_atlas_uri_here"
```

### 4. Create Index for Vector Search

In your MongoDB Atlas UI, create an index for vector search in the rag_v0 collection. The index should include a knnVector field for storing the embeddings. Example configuration:

```bash
{
  "mappings": {
    "dynamic": false,
    "fields": {
      "embedding": {
        "type": "knnVector",
        "dimensions": 384,
        "similarity": "cosine"
      }
    }
  }
}
```

## Usage

### 1. Run the Upload Script

Run upload.py to read the text file, split it into chunks, generate embeddings, and store the results in MongoDB Atlas:

```bash
python upload.py
```

### 2. Run the Query Script

Run query.py to query the MongoDB database using a sample query:

```bash
python query.py
```

### Example Output

After running query.py, you should see output similar to:

```bash
[
    {
        "text": "Deepseek is a term that refers to...",
        "score": 0.92
    },
    {
        "text": "In the context of deep learning, deepseek...",
        "score": 0.89
    },
    {
        "text": "Deepseek uses advanced search techniques...",
        "score": 0.85
    }
]
```