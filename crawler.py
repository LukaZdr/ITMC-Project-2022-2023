# imports
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse

# methods
def accepted_toplevel_domain(link):
	for whitelist_domain in whitelist_domains:
		if link.startswith(whitelist_domain):
			return True
	return False

# setup
# seeds = ['https://www.ekz.de/']
seeds = ['https://en.wikipedia.org/wiki/Beautiful_Soup_(HTML_parser)']
# seeds = ['https://www.ekz.de/news/ausbildung-2023-382']
pending_links = seeds # needs to see all the seed files
seen_links = []
whitelist_domains = list(map(lambda x: 'https://' + urlparse(x).netloc, seeds))

count = 0 # TODO: Remove
while len(pending_links) > 0 and count < 10: # TODO: Remove count
	# load and parse current_link
	current_link = pending_links.pop(0)
	response = requests.get(current_link, allow_redirects=True)
	soup = BeautifulSoup(response.content, 'html.parser')

	# save page content as paragraphs
	paragraphs = []
	paragraph_text = ''
	for line in soup.get_text(separator=" ").split('\n'):
		stripped_line = line.strip()
		if stripped_line == '':
			# save paragraph when it ends
			if paragraph_text != '':
				paragraphs.append(paragraph_text.strip())
				print(paragraph_text.strip())
				print('')
				paragraph_text = ''
			# skip line if it is subsequent newline
			if paragraph_text == '':
				continue
		else:
			paragraph_text = paragraph_text + ' ' + stripped_line


	break
	# add links on site to pending links
	for a in soup.find_all('a', href=True):
		link = a['href']
		# if link is relative make it abolute
		if link.startswith('/'):
			domain = urlparse(current_link).netloc
			link = 'https://' + domain + link
		# only if link has the same toplevel domain
		if not accepted_toplevel_domain(link):
			continue
		# only if link is not seen or pending links
		if link in pending_links or link in seen_links:
			continue
		pending_links.append(link)
	count += 1 # TODO: Remove count

print(len(pending_links))