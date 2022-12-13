import numpy as np
import psycopg2, pickle
from psycopg2 import sql
from modules.crawler import Crawler
from modules.encoder import Encoder
from modules.preprocessor import Preprocessor
from modules.transformer import Transformer
from modules.encoder_flair import EncoderFlair
from modules.clusterer import Clusterer

# Connect to database
conn = psycopg2.connect("dbname='postgres' user='postgres' host='127.0.0.1' password='pw' port='5432'")
cur = conn.cursor()

# Selection
print('Selecting documents')
seed_urls = ['https://de.wikipedia.org/wiki/Webcrawler','https://de.wikipedia.org/wiki/Computerprogramm']
crawler = Crawler()
texts = crawler.run(seed_urls)
# texts = crawler.run(seed_urls, subdomain_whitelist=seed_urls)

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

print('Saving encoding for documents')
# > encode the sentences
encoder = Encoder()

# > get texts from db
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

# Data mining
# > cluster
clusterer = Clusterer()
clusterer.run()

# Interpretation

# Close database connection
conn.commit()
cur.close()
conn.close()
