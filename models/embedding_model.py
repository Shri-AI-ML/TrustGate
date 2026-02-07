# models/embedding_model.py

from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL_NAME, DEVICE
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO)

class EmbeddingModel:
    def __init__(self):
        logging.info(f"Loading embedding model: {EMBEDDING_MODEL_NAME} on {DEVICE}")
        self.model = SentenceTransformer(EMBEDDING_MODEL_NAME, device=DEVICE)
        logging.info("Embedding model loaded successfully.")

    def encode(self, texts):
        """
        Generate embeddings for a single string or list of strings.
        Returns numpy array.
        """
        if isinstance(texts, str):
            texts = [texts]

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=False
        )
        return embeddings


# Singleton pattern (important)
_embedding_model_instance = None

def get_embedding_model():
    global _embedding_model_instance
    if _embedding_model_instance is None:
        _embedding_model_instance = EmbeddingModel()
    return _embedding_model_instance
