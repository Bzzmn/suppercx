from dotenv import load_dotenv
from voyageai import Client
from langchain_core.embeddings import Embeddings
from typing import List
from tqdm import tqdm

load_dotenv()
voyage_client = Client()

class VoyageAIEmbeddings(Embeddings):
    def __init__(self, model: str = "voyage-3-lite", batch_size: int = 128):
        self.model = model
        self.batch_size = batch_size

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        all_embeddings = []
        for i in tqdm(range(0, len(texts), self.batch_size), desc="Embedding documents"):
            batch = texts[i:i+self.batch_size]
            embeddings = voyage_client.embed(batch, model=self.model)
            all_embeddings.extend(embeddings.embeddings)
        return all_embeddings
    
    def embed_query(self, text: str) -> List[float]:
        embedding = voyage_client.embed(text, model=self.model)
        return embedding.embeddings[0] 