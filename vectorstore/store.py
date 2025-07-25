from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np

class SimpleVectorStore:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.texts = []
        self.embeddings = []

    def add_documents(self, texts):
        new_embeddings = self.model.encode(texts)
        self.texts.extend(texts)
        self.embeddings.extend(new_embeddings)

    def query(self, q, top_k=3):
        q_emb = self.model.encode([q])[0]
        sims = cosine_similarity([q_emb], self.embeddings)[0]
        top_indices = np.argsort(sims)[-top_k:][::-1]
        return [self.texts[i] for i in top_indices]