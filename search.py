import psycopg2, pickle
from encoder import Encoder
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import util

# Connect to database
conn = psycopg2.connect("dbname='postgres' user='postgres' host='127.0.0.1' password='pw' port='5432'")
cur = conn.cursor()

encoder = Encoder()
sentence = ['Was ist ein webfeed']
search_embedding = encoder.run(sentence)[0]

current_max_score = 0
winner_id = -1

cur.execute(f'select id, embedding from chunks')
for id, byte_embedding in cur.fetchall():
		embedding = pickle.loads(byte_embedding)
		cosine_scores = util.pytorch_cos_sim(embedding, search_embedding)
		score = cosine_scores.numpy()[0][0]
		if score > current_max_score:
			current_max_score = score
			winner_id = id

print(current_max_score)
print(winner_id)

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