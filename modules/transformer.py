#imports
from nltk.tokenize import sent_tokenize
"""
Problem: big Paragraphs are not good answers so we need to cut them down.

Splits paragraphs up into chunks. each chunk has a max of three sentences.
So a text wit five sentences is saved like this:
(sentence1, sentence2, sentence3),
(sentence2, sentence3, sentence4),
(sentence3, sentence4, sentence5),
"""

# unifys paragraphes for datamining step
class Transformer():
	def __init__(self):
		self.chunk_count = 1
		self.transformed_texts = []
		self.max_sentences_per_chunk = 2
		self.min_words_per_chunk = 6

	def __add_too_result(self, url, paragraph_count, text):
		self.transformed_texts.append({'url': url,
																	 'paragraph_count': paragraph_count,
																	 'chunk_count': self.chunk_count,
																	 'text': text})
		self.chunk_count += 1

	def run(self, preprocessed_paragraphs):
		self.transformed_texts = []
		for paragraph in preprocessed_paragraphs:
			self.chunk_count = 1
			sentences = sent_tokenize(paragraph['text'])
			# paragraph is small enough
			if len(sentences) <= self.max_sentences_per_chunk:
				self.__add_too_result(paragraph['url'],
															paragraph['paragraph_count'],
															paragraph['text'])
			# paragraph has to be split
			else:
				while len(sentences) > self.max_sentences_per_chunk:
					head_sentence = sentences.pop(0)
					tail_sentences = sentences[0:self.max_sentences_per_chunk-1]
					chunk = ' '.join([head_sentence] + tail_sentences)
					self.__add_too_result(paragraph['url'],
																paragraph['paragraph_count'],
																chunk)
		"""
		[
			{url: 'www.url.de', paragraph_count: 1, 'chunk_count': 5 ,text: 'Foo Bar Baz.'},
			{url: 'www.url.de', paragraph_count: 1, 'chunk_count': 6 ,text: 'Foo Bar Baz.'},
		]
		"""
		return self.transformed_texts

	def __enough_words_in_chunk(self, text):
		print('check if enough words are in chunk')
		return False