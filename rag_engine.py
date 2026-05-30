import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.PersistentClient(path="./chroma_data")
collection = client.get_or_create_collection("documents")

def chunk_text(text, size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start+size])
        start += size - overlap
    return chunks

def store_document(doc_id, text):
    chunks = chunk_text(text)
    embeddings = model.encode(chunks).tolist()
    ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
    collection.add(documents=chunks, embeddings=embeddings, ids=ids,
                   metadatas=[{"doc_id": doc_id} for _ in chunks])
    print(f"Stored {len(chunks)} chunks for {doc_id}")

def search_documents(query, top_k=3):
    embedding = model.encode([query]).tolist()
    results = collection.query(query_embeddings=embedding, n_results=top_k)
    return results['documents'][0]