import requests
import time
import re
from bs4 import BeautifulSoup
import pymysql

num = 0
url = 'https://movie.douban.com/top250'
payload = {
   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'
}

def get_html(num):
	r = requests.get(url+'?start='+ str(num) +'&filter=', params = payload)
	return r.content.decode()

def get_data(html):
	soup = BeautifulSoup(html, 'lxml')
	#电影名
	titles = soup.select('span.title')
	global title1, score1, val1, quote1
	title1 = [title.get_text() for title in titles if not title.get_text().startswith('\xa0/')]
	#评分
	scores = soup.select('span.rating_num')
	score1 = [score.get_text() for score in scores]
	#评价人数
	p = re.compile('\d+')
	vals = soup.select('span[content] + span')
	val1 = [p.match(val.get_text()).group() for val in vals]
	#短评
	quotes = soup.select('span.inq')
	quote1 = [quote.get_text() for quote in quotes]

'''
	mode = '{0:^30}\t{1:^10}\t{2:^10}\t{3:<10}\n'
	with open('data.txt', 'a') as f:
		for i in range(25):
			try:
				f.write(mode.format(title1[i], score1[i], val1[i], quote1[i]))
			except UnicodeEncodeError:
				pass
'''

def connect_db():
	conn = pymysql.connect(
		host = '127.0.0.1', 
		port = 3306, 
		user = 'root', 
		password = 'xxx', 
		db = 'douban',
		charset = 'utf8'
	)
	cur = conn.cursor()
	get_data(html)
	for i in range(25):
		ret = cur.execute(
			'insert into top250 (title, score, val, quote) values (%s, %s, %s, %s)', 
			(title1[i], score1[i], val1[i], quote1[i])
		)
	conn.commit()
	cur.close()
	conn.close()

if __name__ == '__main__':
	for num in range(0, 226, 25):
		html = get_html(num)
		connect_db()
		time.sleep(1)
