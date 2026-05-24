from sentence_transformers import SentenceTransformer
import torch
import torch.nn.functional as F

class PyTorchRAGDatabase:
    def __init__(self, model: str = 'all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name_or_path=model)
        self.chunks: list[str] = []
        self.embed = None

    
    def load_and_chunk_text(self, filepath: str, chunk_size: int, overlap: int):
        try:
            with open(filepath, 'r') as file:
                content = file.read()
                i = 0
                words = content.split()
                length = len(words)
                while i<length:
                    chunk = words[i:i+chunk_size]
                    chunk = " ".join(chunk)
                    self.chunks.append(chunk)
                    i += chunk_size-overlap
        except FileNotFoundError as error:
            raise FileNotFoundError(f"File in this path doesn't exist. {error}")
        

    def get_embeddings(self):
        if self.chunks:
            self.embed = self.model.encode(self.chunks, convert_to_tensor = True)


    def search(self, query: str):
        if query:
            embed_query  = self.model.encode(query, convert_to_tensor = True)
            embed_query = embed_query.unsqueeze(0)
            sim = F.cosine_similarity(self.embed, embed_query)
            index = torch.argmax(sim)
            return self.chunks[index.item()]