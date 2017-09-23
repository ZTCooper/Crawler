import urllib.request   #请求访问url的包
import urllib.parse     #负责解析的包
import json

content = input('请输入需要翻译的内容：')
url ='http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&sessionFrom='

#Form表单
data = {}
data['i'] = content
data['from'] = 'AUTO'
data['to'] = 'AUTO'
data['smartresult'] = 'dict'
data['client'] = 'fanyideskweb'
data['salt'] = '1505821579753'
data['sign'] = 'f4ff939bbaf67c8d83efd17ee8d82c0b'
data['doctype'] = 'json'
data['version'] = '2.1'
data['keyfrom'] = 'fanyi.web'
data['action'] = 'FY_BY_CLICKBUTTION'
data['typoResult'] = 'true'

data = urllib.parse.urlencode(data).encode('utf-8')     #编码

response = urllib.request.urlopen(url,data)
html = response.read().decode('utf-8')       #解码为unicode

target = json.loads(html)
print('翻译结果：%s' % (target["translateResult"][0][0]['tgt']))

