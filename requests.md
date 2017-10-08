# Requests
  
* [基本用法](#1)  
* [高级用法](#2)
  

## 基本用法 <a id="1"></a>
```python
import requests

r = requests.get('https://github.com/ZTCooper')
print(r.text)
```
  
```python
payload = {
    'key':'value'
}
r = requests.get('https://github.com/ZTCooper', params = payload)
print(r.url) 

# https://github.com/ZTCooper?key=value 
``` 
  
```python  
r.encoding = 'utf-8'
r.content
```   
  
```python
#二进制数据创建图片

from PIL import Image
from io import BytesIO

im = Image.open(BytesIO(r.content))
```  
  
```python
r.json()
r.status_code
r.raise_for_status()
```  
  
```python
#获取原始套接字，设置stream = True

r = requests.get('https://github.com/ZTCooper', stream = True)
print(r.raw)
print(r.raw.read(10))

#<requests.packages.urllib3.response.HTTPResponse object at 0x0000021C0A28D6A0>
b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x00\x03'  
```
  
```python
#将文本流保存到文件

with open(filename, 'wb') as f:
    for chunk in r.iter_content(chunk_size):
        f.write(chunk)
```  
  
```python
#定制headers 

url = 'https://github.com/ZTCooper'
headers = {'user-agent':'my-app/0.0.1'}
r = requests.get(url, headers = headers)
```
  
```python
#发送更加复杂的POST请求

payload = {'key1': 'value1', 'key2': 'value2'}
r = requests.post('http://httpbin.org/post', data = payload)
print(r.text)
'''
{
...
  "form": {
    "key1": "value1",
    "key2": "value2"
  },
...
}
'''
```  
   
```python
#对dict编码
r = requests.post(url, json.dumps(payload))
#可直接用json传递参数
r = requests.post(url, json = payload)
```
  
```
#POST一个Multipart-Encoded的文件

url = 'http://httpbin.org/post'
files = {'file' : open('test.txt', 'rb')}

r = requests.post(url, files = files)
print(r.text)
'''
{
  ...
  "files": {
    "file": "<censored...binary...data>"
  },
  ...
}
'''
```  
  
```python
#响应状态码

r.status_code
r.status_code == requests.codes.ok

#通过Response.raise_for_status()抛出异常  
```  
  
```python
#响应头

r.headers
#dict
r.headers['conteny-type']
#'application/json'
r.headers.get('Content-type')
#'application/json'
```  
  
```python
#Cookies

url = 'https://github.com/ZTCooper'
r = requests.get(url)

r.cookies['cookie_name']

#'cookie_value'
#Cookie的返回对象为RequestsCookieJar，类字典
```  
  
```python
#发送cookies

url = 'http://httpbin.org/cookies'
cookies = dict(cookies_are = 'working')

r = requests.get(url, cookies = cookies)
r.text

#'{"cookies": {"cookies_are": "working"}}'
```  
  
```python
#可以把Cookie Jar传到Requests中

jar = requests.cookie.RequestsCookieJar()
jar.set('tasty_cookie', 'yum', domain = 'httpbin.org', path = '/cookies')
jar.set('gross_cookie', 'blech', domain = 'httpbin.org', path = '/elsewhere')
url = 'http://httpbin.org/cookies'
r = requests.get(url, cookies = jar)
r.text

#'{"cookies": {"tasty_cookie": "yum"}}'
#不懂=_=
```
  
```python
#重定向与请求历史

>>> r = requests.get('https://github.com')
>>> r.status_code
200
>>> r.history
[]
#禁用/启用重定向
r = requests.get('https://github.com', allow_redirects = False)
```
  
```python
#timeout

requests.get('https://github.com', timeout = 0.001)
```
  
  
  
## 高级用法 <a id="2"></a>
```python
#会话对象


