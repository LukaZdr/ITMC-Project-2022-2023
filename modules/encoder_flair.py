from flair.data import Sentence
from flair.embeddings import WordEmbeddings, FlairEmbeddings, StackedEmbeddings, DocumentPoolEmbeddings

class EncoderFlair():
  def __init__(self):
    # self.model = FlairEmbeddings('de-forward') # https://github.com/flairNLP/flair/blob/master/resources/docs/embeddings/FLAIR_EMBEDDINGS.md
    self.model = StackedEmbeddings([
                                    FlairEmbeddings('de-forward'),
                                    FlairEmbeddings('de-backward'),
                                   ])
    self.document_embeddings = DocumentPoolEmbeddings([self.model])


  def run(self, texts):
    embeddings = []
    for text in texts:
      sentence = Sentence(text)
      self.document_embeddings.embed(sentence)
      embeddings.append(sentence.embedding.numpy())
    return embeddings