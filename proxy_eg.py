import urllib.request
import random

url = 'http://www.whatismyip.com.tw'    #显示当前访问IP

iplist = ['153.34.202.68:80', '61.135.217.7:80', '120.78.15.63:80']

proxy_support = urllib.request.ProxyHandler({'https:':random.choice(iplist)})

opener = urllib.request.build_opener(proxy_support)     #创建一个opener
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586')]

urllib.request.install_opener(opener)       #安装opener

response = urllib.request.urlopen(url)
html = response.read().decode('utf-8')      #解码

print(html)
