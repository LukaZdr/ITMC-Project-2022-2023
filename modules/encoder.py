from sentence_transformers import SentenceTransformer

class Encoder():
  def __init__(self):
    self.model = SentenceTransformer('Sahajtomar/German-semantic') # https://huggingface.co/Sahajtomar/German-semantic

  def run(self, texts):
    embeddings = []
    embeddings = self.model.encode(texts, convert_to_tensor=True)
    return embeddings