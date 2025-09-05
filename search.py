import faiss
import numpy as np

class FaissIndex:
    def __init__(self, dimension):
        self.index = faiss.IndexFlatL2(dimension)

    def add_embeddings(self, embeddings):
        self.index.add(np.array(embeddings))

    def search(self, query_embedding, top_k=5):
        D, I = self.index.search(np.array(query_embedding), top_k)
        return I[0]
