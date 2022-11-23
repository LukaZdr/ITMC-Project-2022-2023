import psycopg2
from psycopg2 import sql
from crawler import Crawler
from transformer import Transformer
from preprocessor import Preprocessor

# Connect to database
conn = psycopg2.connect("dbname='postgres' user='postgres' host='127.0.0.1' password='pw' port='5432'")
cur = conn.cursor()

# Selection
seed_urls = ['https://en.wikipedia.org/wiki/Beautiful_Soup_(HTML_parser)']
crawler = Crawler()
texts = crawler.run(seed_urls)

# Preprocessing
preprocessor = Preprocessor()
preprocessed_paragraphs = preprocessor.run(texts)

# Transformation
transformer = Transformer()
transformed_texts = transformer.run(preprocessed_paragraphs)
commit_count = 0
for chunk in transformed_texts:
	# Save transformed data to database
	values = [chunk['url'], chunk['text'], chunk['paragraph_count'], chunk['chunk_count']]
	insert = sql.SQL("""insert into chunks (url, text, paragraph_count, chunk_count)
															 values ({})
															 on conflict do nothing""").format(sql.SQL(', ').join(sql.Placeholder() * len(values)))
	cur.execute(insert, values)
	commit_count += 1
	if commit_count%100 == 0:
		conn.commit()

# Data mining

# Interpretation


# Close database connection
conn.commit()
cur.close()
conn.close()