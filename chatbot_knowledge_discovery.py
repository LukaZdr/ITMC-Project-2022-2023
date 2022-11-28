import io
import psycopg2
import psycopg2
import pickle
from tqdm import tqdm
from psycopg2 import sql
from crawler import Crawler
from encoder import Encoder
from transformer import Transformer
from preprocessor import Preprocessor

# Connect to database
conn = psycopg2.connect("dbname='postgres' user='postgres' host='127.0.0.1' password='pw' port='5432'")
cur = conn.cursor()

# # Selection
# print('Selecting documents')
# seed_urls = ['https://en.wikipedia.org/wiki/Beautiful_Soup_(HTML_parser)']
# crawler = Crawler()
# texts = crawler.run(seed_urls)

# # Preprocessing
# print('Preprocessing selecting documents')
# preprocessor = Preprocessor()
# preprocessed_paragraphs = preprocessor.run(texts)

# # Transformation
# print('Transforming preprocessed documents')
# transformer = Transformer()
# transformed_texts = transformer.run(preprocessed_paragraphs)
# commit_count = 0
# print('Saving transformed documents')
# for chunk in transformed_texts:
# 	# Save transformed data to database
# 	values = [chunk['url'], chunk['text'], chunk['paragraph_count'], chunk['chunk_count']]
# 	insert = sql.SQL("""insert into chunks (url, text, paragraph_count, chunk_count)
# 															 values ({})
# 															 on conflict do nothing""").format(sql.SQL(', ').join(sql.Placeholder() * len(values)))
# 	cur.execute(insert, values)
# 	commit_count += 1
# 	if commit_count%100 == 0:
#			print(commit_count)
# 		conn.commit()

# Data mining
print('Saving encoding for documents')
# > encode the sentences
encoder = Encoder()

# > get texts from db
cur.execute('select id, text from chunks where id=1 limit 1')
chunks = cur.fetchall()

commit_count = 0
for id, text in chunks:
	embedding = encoder.run([text])
	byte_vector = pickle.dumps(embedding)
	# save embedding back to db
	update = sql.SQL("update chunks SET embedding = {} where id = {};").format(
            sql.Placeholder(), sql.Placeholder())
	cur.execute(update, [byte_vector, id])
	commit_count += 1
	if commit_count%100 == 0:
		print(commit_count)
		conn.commit()

### TEST IF PICKELING WORKS IN DB
# from sentence_transformers import util
# cur.execute(f'select embedding from chunks where id={1} and embedding is not null limit 1')
# b = cur.fetchall()
# for byte_embedding in b:
# 		embedding = pickle.loads(byte_embedding[0])
# 		cosine_scores = util.pytorch_cos_sim(embedding, a_embedding)
# 		print(cosine_scores)

# > cluster
# > > k-means shizzle

# Interpretation


# Close database connection
conn.commit()
cur.close()
conn.close()