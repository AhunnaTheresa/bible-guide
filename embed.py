import chromadb
from sentence_transformers import SentenceTransformer
from ingest import load_and_chunk_bible
import os

print("Loading Bible chunks...")
chunks = load_and_chunk_bible('data/KJV.json')
print(f"Loaded {len(chunks)} chunks")

print("Loading embedding model...")
model = SentenceTransformer('all-MiniLM-L6-v2')

print("Setting up ChromaDB...")
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection(name="bible")

print("Embedding and storing chunks (this will take several minutes)...")
batch_size = 100
for i in range(0, len(chunks), batch_size):
    batch = chunks[i:i + batch_size]
    texts = [c['text'] for c in batch]
    embeddings = model.encode(texts).tolist()
    ids = [f"chunk_{i+j}" for j in range(len(batch))]
    metadatas = [{'source': c['source'], 'book': c['book'], 'chapter': str(c['chapter'])} for c in batch]
    collection.add(documents=texts, embeddings=embeddings, ids=ids, metadatas=metadatas)
    if (i // batch_size) % 10 == 0:
        print(f"Progress: {i}/{len(chunks)} chunks embedded...")

print(f"Done! {collection.count()} chunks stored in ChromaDB.")
