# imports
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse

class Crawler():
	def __accepted_domain(self, link, whitelist_domains):
		for whitelist_domain in whitelist_domains:
			if link.startswith(whitelist_domain):
				return True
		return False

	def run(self, seed_urls):
		# setup
		pending_links = seed_urls # needs to see all the seed files
		seen_links = []
		whitelist_domains = list(map(lambda x: 'https://' + urlparse(x).netloc, seed_urls))
		crawled_texts = []

		count = 0 # TODO: Remove
		while len(pending_links) > 0 and count < 10: # TODO: Remove count
			# load and parse current_link
			current_link = pending_links.pop(0)
			response = requests.get(current_link, allow_redirects=True)
			soup = BeautifulSoup(response.content, 'html.parser')

			# save page content for next step
			crawled_texts.append({'url': current_link, 'text': soup.get_text(separator=" ")})

			# add links on site to pending links
			for a in soup.find_all('a', href=True):
				link = a['href']
				# if link is relative make it abolute
				if link.startswith('/'):
					domain = urlparse(current_link).netloc
					link = 'https://' + domain + link
				# only if link has the same toplevel domain
				if not self.__accepted_domain(link, whitelist_domains):
					continue
				# only if link is not seen or pending links
				if link in pending_links or link in seen_links:
					continue
				pending_links.append(link)
			count += 1 # TODO: Remove count
		"""
			[
				{'url': 'www.url.de', 'text': 'Foo Bar Baz.'},
				{'url': 'www.url.de', 'text': 'Foo Bar Baz.'}
			]
		"""
		return crawled_texts
