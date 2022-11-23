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
	def run(self, preprocessed_paragraphs):
		transformed_texts = []
		for paragraph in preprocessed_paragraphs:
			sentences = sent_tokenize(paragraph)
			# paragraph is small enough
			if len(sentences) < 4:
				transformed_texts.append(preprocessed_paragraphs)
			#paragraph has to be split
			else:
				while len(sentences) > 3:
					first_tentence = sentences.pop(0)
					second_and_third_sentence = sentences[0:2]
					chunk = ' '.join([first_tentence] + second_and_third_sentence)
					transformed_texts.append((chunk))
		return transformed_texts