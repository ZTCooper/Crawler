import scrapy
from bs4 import BeautifulSoup

from dmoz.items import DmozItem          #导入 Item

class DmozSpider(scrapy.Spider):         #继承于scrapy.Spider
    name = 'dmoz'                        
    allowed_domains = ['dmoztools.net']     
    start_urls = [
        'http://dmoztools.net/Computers/Programming/Languages/Python/Books/',
        'http://dmoztools.net/Computers/Programming/Languages/Python/Resources/'
        ]

    def parse(self, response):   

        soup = BeautifulSoup(response.body)
        
        items = []

        length = len(soup.select('div .title-and-desc'))
        
        for i in range(length):
            item = DmozItem()
            
            item['title'] = soup.select('div .site-title')[i].string
                                             #.string获得节点内容
            item['link'] = soup.select('div .title-and-desc > a')[i].get('href')
                                        #div标签下class=title-and-desc的直接子标签为'a'的
                                        #.get('href')得到链接
            item['desc'] = soup.select('div .site-descr')[i].get_text()
                                            #.get_text()得到内容
            items.append(item)

        return items


