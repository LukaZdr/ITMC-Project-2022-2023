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
						paragraphs.append({'url': document_dict['url'],
															 'paragraph_count': paragraph_count,
															 'text': paragraph_text.strip()})
						paragraph_count += 1
						paragraph_text = ''
					# skip line if it is subsequent newline
					if paragraph_text == '':
						continue
				else:
					paragraph_text = paragraph_text + ' ' + stripped_line
		"""
		[
			{url: 'www.url.de', paragraph_count: 1, text: 'Foo Bar Baz.'},
			{url: 'www.url.de', paragraph_count: 1, text: 'Foo Bar Baz.'}
		]
		"""
		return paragraphs