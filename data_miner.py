from sentence_transformers import SentenceTransformer, util

class DataMiner():
  def similarity(vec_list_1,vec_list_2):
    cosine_scores = util.pytorch_cos_sim(vec_list_1, vec_list_2)
    for i in range(len(sentences1)):
        for j in range(len(sentences2)):
            print(cosine_scores[i][j])