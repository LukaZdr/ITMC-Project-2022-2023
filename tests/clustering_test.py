from sklearn.cluster import DBSCAN
from sentence_transformers import util
import numpy as np
import psycopg2
import pickle

# Connect to database
conn = psycopg2.connect("dbname='postgres' user='postgres' host='127.0.0.1' password='pw' port='5432'")
cur = conn.cursor()

cur.execute(f'select id, embedding from chunks')
db_embeddings = cur.fetchall()
embeddings = []

print('load embedding from db')
for id, byte_embedding in db_embeddings:
  embedding = pickle.loads(byte_embedding)
  if embeddings == []:
    embeddings = embedding.numpy()
  else:
    embeddings = np.append(embeddings, embedding.numpy(), axis=0)



print('initiate_cluster')
clustering = DBSCAN(eps=15, min_samples=2).fit(embeddings)
print(clustering.labels_)
print(clustering)