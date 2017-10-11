import requests
from bs4 import BeautifulSoup
import random
import datetime

random.seed(datetime.datetime.now())

def get_links(start_url = r'https://en.wikipedia.org/wiki/Eric_Idle'):
	links = []
	html = requests.get(start_url)
	soup = BeautifulSoup(html.text)
	for link in soup.select('div#bodyContent a'):
		if 'href' in link.attrs:
			#print(link.attrs['href'])
			if link.get('href').startswith('/wiki') and link.get('href') not in links:
				#href = re.compile(r'^(/wiki?)(?!:)*$')
				links.append(link.get('href'))
	return(links)

urls = get_links()
while len(urls):
	new_link = urls[random.randint(0,len(urls)-1)]
	print(new_link)
	urls = get_links('https://en.wikipedia.org'+new_link)
	print(len(urls))
	break


'''
def serch_4_target(target = r'https://en.wikipedia.org/wiki/Kevin_bacon'):
	urls = get_links()
	for url in urls:
		if url == traget:
			return
		else:
			get_links(url)
'''