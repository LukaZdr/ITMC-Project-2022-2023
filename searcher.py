import psycopg2, pickle
from encoder import Encoder
from sentence_transformers import util

class Searcher():
	def __init__(self, result_count=5):
		self.result_count = result_count
		# Connect to database
		conn = psycopg2.connect("dbname='postgres' user='postgres' host='127.0.0.1' password='pw' port='5432'")
		self.cur = conn.cursor()
		self.encoder = Encoder()

	def run(self, sentence):
		search_embedding = self.encoder.run([sentence])[0]
		return self.similar_texts_for_embedding(search_embedding)

	def similar_texts_for_embedding(self, embedding):
		similarities = []
		self.cur.execute(f'select id, embedding from chunks')
		for id, byte_embedding in self.cur.fetchall():
				db_embedding = pickle.loads(byte_embedding)
				cosine_scores = util.pytorch_cos_sim(db_embedding, embedding)
				score = cosine_scores.numpy()[0][0]
				similarities.append((id, score))
		similarities.sort(key=lambda a: a[1], reverse=True)
		top_x_results = similarities[:self.result_count]
		return list(map(lambda x: (self.__text_for_id(x[0]), x[1]), top_x_results))

	def __text_for_id(self, id):
		self.cur.execute(f'select text from chunks where id = {id} limit 1')
		return self.cur.fetchone()[0]

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
