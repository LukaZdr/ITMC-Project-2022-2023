# preprocesses the data
class Preprocessor():
	def run(self, texts):
		# save page content as paragraphs
		paragraphs = []
		paragraph_text = ''
		for text in texts:
			for line in text.split('\n'):
				stripped_line = line.strip()
				if stripped_line == '':
					# save paragraph when it ends
					if paragraph_text != '':
						if len(paragraph_text.split(' ')) < 6: # fillter out all text with to few words
							continue
						paragraphs.append(paragraph_text.strip())
						paragraph_text = ''
					# skip line if it is subsequent newline
					if paragraph_text == '':
						continue
				else:
					paragraph_text = paragraph_text + ' ' + stripped_line
		return paragraphs