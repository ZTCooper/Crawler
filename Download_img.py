import urllib.request

response = urllib.request.urlopen('https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1505828521803&di=b0ed9b3d2d7dacbde0156c6397881469&imgtype=0&src=http%3A%2F%2Fpic.58pic.com%2F58pic%2F16%2F42%2F96%2F56e58PICAu9_1024.jpg')

#返回对象
#req = urllib.request.Request('https://...')
#response = urllib.request.urlopen(req)

img = response.read()
with open('github.jpg', 'wb') as f:
	f.write(img)
