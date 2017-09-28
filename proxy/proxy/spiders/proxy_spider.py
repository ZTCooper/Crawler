import scrapy
from bs4 import BeautifulSoup

from proxy.items import ProxyItem

class ProxySpider(scrapy.Spider):
	name = 'proxy'
	allowed_domains= ['xicidaili.com']
	start_urls = [
		'http://www.xicidaili.com/'
		]

	def parse(self, response):
		soup = BeautifulSoup(response.body)
		items = []

		for i in range(len(soup.select('.country + td'))):
									#class = country的下一个兄弟标签
			item = ProxyItem()

			if i%2 == 0:
				item['adrs'] = soup.select('.country + td')[i].get_text()
				item['port'] = soup.select('.country + td + td')[i].get_text()
				item['_type'] = soup.select('.country + td')[i+1].get_text()
				items.append(item)

		return items
		 