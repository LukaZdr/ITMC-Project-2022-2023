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
			if len(sentences) < 4:
				self.__add_too_result(paragraph['url'],
															paragraph['paragraph_count'],
															paragraph['text'])
			# paragraph has to be split
			else:
				while len(sentences) > 3:
					first_tentence = sentences.pop(0)
					second_and_third_sentence = sentences[0:2]
					chunk = ' '.join([first_tentence] + second_and_third_sentence)
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