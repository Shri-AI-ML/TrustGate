import faiss
import numpy as np
from models.embedding_model import get_embedding_model

class RetrievalEngine:
    def __init__(self, chunks):
        self.model = get_embedding_model()
        self.chunks = chunks

        texts = [chunk["text"] for chunk in chunks]
        embeddings = self.model.encode(texts)

        self.dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(np.array(embeddings))

    def retrieve(self, query, top_k=3):
        query_embedding = self.model.encode(query)

        distances, indices = self.index.search(query_embedding, top_k)

        results = []

        for i, idx in enumerate(indices[0]):
            results.append({
                "text": self.chunks[idx]["text"],
                "page_number": self.chunks[idx]["page_number"],
                "distance": distances[0][i]  # smaller = more similar
            })

        return results

