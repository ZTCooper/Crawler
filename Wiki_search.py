# -*- coding: utf-8 -*-
#Wikipedia's six degrees of separation
#找出维基百科中Kevin_Bacon词条与其他词条之间最短链接路径
#广度优先搜索算法(BFS)
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

import pymysql

conn = pymysql.connect(
	host = '127.0.0.1',
	port = 3306,
	user = 'root',
	passwd = 'xxx',
	db = 'wiki',
	charset = 'utf8mb4'
	)
cur = conn.cursor()

class SolutionFound(RuntimeError):
	def __init__(self, message):
		self.message = message

def getLinks(fromPageId):
	cur.execute('select toPageId from links where fromPageId = %s', (fromPageId))
	if cur.rowcount == 0:
		return None
	else:
		return [x[0] for x in cur.fetchall()]

def constructDict(currentPageId):
	links = getLinks(currentPageId)
	if links:
		return dict(zip(links, [{}]*len(links)))
	return {}

#链接树要么为空，要么包含多个链接
def searchDepth(targetPageId, currentPageId, linkTree, depth):
	if depth == 0:
		#停止递归，返回结果
		return linkTree

	if not linkTree:
		linkTree = constructDict(currentPageId)
		if not linkTree:
		#若此节点页面无链接，则跳过
			return {}

	if targetPageId in linkTree.keys():
		print('TARGET' + str(targetPageId) + 'FOUND!')
		raise solutionFound('PAGE:' + str(currentPageId))
		for branchKey, branchValue in linkTree.items():
			try:
				#递归建立链接树
				linkTree[branchKey] = searchDepth(targetPageId, branchKey, branchValue, depth - 1)
			except 	SolutionFound as e:
				print(e.message)
				raise SolutionFound('PAGE' + str(currentPageId))
	return linkTree

try:
	searchDepth(134951, 1, {}, 4)
	print('No solution found')
except SolutionFound as e:
	print(e.message)
