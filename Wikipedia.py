# -*- coding: utf-8 -*-
#Wikipedia's six degrees of separation
#把数据存入数据库
'''
mysql> describe links;				mysql> describe pages;
+------------+-----------+			+---------+--------------+
| Field      | Type      |			| Field   | Type         |
+------------+-----------+			+---------+--------------+
| id         | int(11)   |			| id      | int(11)      |
| fromPageId | int(11)   |			| url     | varchar(255) |
| toPageId   | int(11)   |			| created | timestamp    |
| created    | timestamp |			+---------+--------------+
+------------+-----------+
'''

import requests
from bs4 import BeautifulSoup
import pymysql


#将数据存入database:'wiki'，table:(pages, links)
#连接到数据库
conn = pymysql.connect(
	host = '127.0.0.1',
	port = 3306,
	user = 'root',
	passwd = 'xxx',
	db = 'wiki',
	charset = 'utf8mb4'
	)#most bytes 4 存储4字节
#创建游标
cur = conn.cursor()

#如果数据库中不存在则将page存入
def insert_page_IfNotExists(url):
	cur.execute('select * from pages where url = %s', (url))
	if cur.rowcount == 0:	#该page不存在
		cur.execute('insert into pages (url) values (%s)', (url))	#存入
		conn.commit()	#提交
		return cur.lastrowid
	else:
		return cur.fetchone()[0]	#将返回元组中数据提取为字符串

#存入links
def insert_link(fromPageId, toPageId):
	cur.execute('select * from links where fromPageId = %s and toPageId = %s',
		(int(fromPageId), int(toPageId)))
	if cur.rowcount == 0:	#链接不存在
		cur.execute('insert into links (fromPageId, toPageId) values(%s, %s)',
			(int(fromPageId), int(toPageId)))	#存入
		conn.commit()	#提交


pages = set()
def get_links(pageUrl, recursionLevel):
	global pages
	if recursionLevel > 4:
		return
	pageId = insert_page_IfNotExists(pageUrl)	
				#第一次返回‘/wiki/Kevin_Bacon’的id
	headers = {'user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}
	html = requests.get('http://en.wikipedia.org' + pageUrl, headers = headers)
	soup = BeautifulSoup(html.text, 'lxml')
	for link in soup.select('div#bodyContent a'):
		if 'href' in link.attrs:
			if link.get('href').startswith('/wiki'):
				insert_link(pageId, insert_page_IfNotExists(link.get('href')))
				if link.get('href') not in pages:
					#遇到新页面，加入set并搜索里面的链接
					new_page = link.get('href')
					pages.add(new_page)
					get_links(new_page, recursionLevel + 1)


get_links('/wiki/Kevin_Bacon', 0)
cur.close()		#关闭指针对象
conn.close()	#关闭连接对象

