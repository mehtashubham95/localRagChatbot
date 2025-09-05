from sentence_transformers import SentenceTransformer
import numpy as np
import pickle
import os

class TextEmbedder:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.embedder = SentenceTransformer(model_name)

    def embed_chunks(self, chunks):
        return self.embedder.encode(chunks)

    def save_embeddings(self, embeddings, chunks, emb_path='chunk_embeddings.npy', chunks_path='all_chunks.pkl'):
        np.save(emb_path, embeddings)
        with open(chunks_path, 'wb') as f:
            pickle.dump(chunks, f)

    def load_embeddings(self, emb_path='chunk_embeddings.npy', chunks_path='all_chunks.pkl'):
        if os.path.exists(emb_path) and os.path.exists(chunks_path):
            embeddings = np.load(emb_path)
            with open(chunks_path, 'rb') as f:
                chunks = pickle.load(f)
            print("Loaded cached embeddings and chunks.")
            return embeddings, chunks
        else:
            return None, None