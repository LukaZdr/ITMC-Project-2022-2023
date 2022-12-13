import re
# preprocesses the data
class Preprocessor():
	def run(self, documents):
		# save page content as paragraphs
		paragraphs = []
		paragraph_text = ''
		for document_dict in documents:
			paragraph_count = 1
			for line in document_dict['text'].split('\n'):
				stripped_line = line.strip()
				if stripped_line == '':
					# save paragraph when it ends
					if paragraph_text != '':
						if len(paragraph_text.split(' ')) < 6: # fillter out all text with to few words
							continue
						cleaned_paragraph = self.__clean_paragraph(paragraph_text)
						paragraphs.append({'url': document_dict['url'],
															 'paragraph_count': paragraph_count,
															 'text': cleaned_paragraph})
						paragraph_count += 1
						paragraph_text = ''
					# skip line if it is subsequent newline
					if paragraph_text == '':
						continue
				else:
					paragraph_text = paragraph_text + ' ' + stripped_line # add sentence to curren paragraph
		"""
		[
			{url: 'www.url.de', paragraph_count: 1, text: 'Foo Bar Baz.'},
			{url: 'www.url.de', paragraph_count: 1, text: 'Foo Bar Baz.'}
		]
		"""
		return paragraphs

	def __clean_paragraph(self, paragraph):
		# strip
		stripped_paragraph = paragraph.strip()
		# get rid of special chars
		removed_special_chars = re.sub(r"[^\sa-zA-Z,.:()-\/]", '', stripped_paragraph)
		# get rid of multiple whitespaces
		removed_multi_whitespaces = re.sub(r"\s{2,}", ' ', removed_special_chars)
		return removed_multi_whitespaces