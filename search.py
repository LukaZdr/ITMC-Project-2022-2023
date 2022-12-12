import psycopg2, pickle
from encoder_flair import EncoderFlair
from encoder import Encoder
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import util

# setup
result_count = 5

# Connect to database
conn = psycopg2.connect("dbname='postgres' user='postgres' host='127.0.0.1' password='pw' port='5432'")
cur = conn.cursor()

encoder = Encoder()
sentence = ['wer hat HTML entwickelt?']
search_embedding = encoder.run(sentence)[0]

similarities = []

cur.execute(f'select id, embedding from chunks')
for id, byte_embedding in cur.fetchall():
		embedding = pickle.loads(byte_embedding)
		cosine_scores = util.pytorch_cos_sim(embedding, search_embedding)
		score = cosine_scores.numpy()[0][0]
		similarities.append((id, embedding, score))

similarities.sort(key=lambda a: a[2], reverse=True)
top_x_results = similarities[:result_count]

for id, embedding, score in top_x_results:
	print(id, score)




# print(cosine_similarity(list,list))


# mit 3 sätzen pro chunk

# wer hat HTML entwickelt?
# Das  World Wide Web Consortium  (W3C), das heute von Tim Berners-Lee, dem Erfinder des WWW, geleitet wird, und andere entwickeln den HTML- und den CSS-Standard; andere Standards kommen von der  Internet Engineering Task Force , der  ECMA  und Herstellern wie  Sun Microsystems .
# Nicht vom  W3-Konsortium  standardisiert ist  JavaScript , die am weitesten verbreitete Skript- oder Makrosprache von Webbrowsern.
# JavaScript  ist eine  Skriptsprache  mit Anweisungen für den  Browser , mit der Programme (Skripte) eingebettet werden können.

# Wer entwickelte den NeXT-Computer?
# Berners-Lee entwickelte dazu das HTTP -Netzwerkprotokoll und die Textauszeichnungssprache HTML .
# Zudem programmierte er den ersten Webbrowser und die erste Webserver-Software.
# Er betrieb auch den ersten Webserver der Welt auf seinem Entwicklungsrechner vom Typ  NeXTcube .

# mit 1 satz pro chunk

# wer hat HTML entwickelt?
# Die Grundtechniken sind hierbei  HTML ,  CSS  und oft auch  JavaScript .

# Wer entwickelte den NeXT-Computer?
# Er betrieb auch den ersten Webserver der Welt auf seinem Entwicklungsrechner vom Typ  NeXTcube .
