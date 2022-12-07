import psycopg2, pickle
import numpy as np
from psycopg2 import sql
from crawler import Crawler
from encoder import Encoder
from transformer import Transformer
from preprocessor import Preprocessor

# Connect to database
conn = psycopg2.connect("dbname='postgres' user='postgres' host='127.0.0.1' password='pw' port='5432'")
cur = conn.cursor()

# Selection
print('Selecting documents')
seed_urls = ['https://de.wikipedia.org/wiki/Webcrawler']
crawler = Crawler()
texts = crawler.run(seed_urls)

# Preprocessing
print('Preprocessing selecting documents')
preprocessor = Preprocessor()
preprocessed_paragraphs = preprocessor.run(texts)

# Transformation
print('Transforming preprocessed documents')
transformer = Transformer()
transformed_texts = transformer.run(preprocessed_paragraphs)
commit_count = 0
print('Saving transformed documents')
for chunk in transformed_texts:
	# Save transformed data to database
	values = [chunk['url'], chunk['text'], chunk['paragraph_count'], chunk['chunk_count']]
	insert = sql.SQL("""insert into chunks (url, text, paragraph_count, chunk_count)
															 values ({})
															 on conflict do nothing""").format(sql.SQL(', ').join(sql.Placeholder() * len(values)))
	cur.execute(insert, values)
	commit_count += 1
	if commit_count%100 == 0:
		print(commit_count)
		conn.commit()
conn.commit()

# Data mining
print('Saving encoding for documents')
# > encode the sentences
encoder = Encoder()

# # > get texts from db
cur.execute('select id, text from chunks')
chunks = cur.fetchall()

commit_count = 0
for id, text in chunks:
	embedding = encoder.run([text])
	byte_vector = pickle.dumps(embedding)
	# save embedding back to db
	update = sql.SQL("update chunks SET embedding = {} where id = {};").format(sql.Placeholder(), sql.Placeholder())
	cur.execute(update, [byte_vector, id])
	commit_count += 1
	if commit_count%100 == 0:
		print(commit_count)
		conn.commit()
conn.commit()

# > cluster
# load all clusters from db
cur.execute(f'select id, embedding from chunks')
byte_embeddings = cur.fetchall()
document_vectors = np.array(list(map(lambda x: pickle.loads(x[1]).numpy()[0], byte_embeddings)))

# k means version
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=20, random_state=0).fit(document_vectors)
# kmeans.labels_
print(kmeans.cluster_centers_)

# find vector in db
for id, byte_embedding in byte_embeddings:
	db_vector = pickle.loads(byte_embedding).numpy()[0]
	if db_vector in kmeans.cluster_centers_:
		print(id)

# Db scan version
from sklearn.cluster import DBSCAN

# Interpretation


# Close database connection
conn.commit()
cur.close()
conn.close()
