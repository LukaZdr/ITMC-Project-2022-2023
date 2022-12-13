import numpy as np
import pickle, psycopg2
from sklearn.cluster import KMeans
from searcher import Searcher

class Clusterer():
  def __init__(self, algorithm='kmeans'):
    self.algorith = algorithm
    conn = psycopg2.connect("dbname='postgres' user='postgres' host='127.0.0.1' password='pw' port='5432'")
    self.cur = conn.cursor()
    self.searcher = Searcher()

  def run(self):
    # load data from database
    self.cur.execute(f'select id, embedding from chunks')
    byte_embeddings = self.cur.fetchall()
    id_and_embedding = np.array(list(map(lambda x: (x[0], pickle.loads(x[1]).numpy()[0]), byte_embeddings)))
    embeddings = np.array(list(map(lambda x: x[1], id_and_embedding)))

    # cluster
    kmeans = KMeans(n_clusters=20, random_state=0).fit(embeddings)
    print(kmeans.cluster_centers_)

    # find vector in db
    for index, cluster_embedding in enumerate(kmeans.cluster_centers_):
      print(f'Intent-{index}')
      print(self.searcher.similar_texts_for_embedding(cluster_embedding))
      print('==========================================================')
    # self.__ids_for_embedding_list(kmeans.cluster_centers_, id_and_embedding)

  def  __ids_for_embedding_list(self, cluster_centers, id_and_embedding):
    for id, embedding in id_and_embedding:
      if embedding in cluster_centers:
        print(id)
