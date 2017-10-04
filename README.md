# crawler&scrapy
***09.19.2017***  
Just to record my every crawler from the very beginning.

***10.04.2017***  
**Scrapy工作原理示意图**  
![](Image.png 'scrapy工作原理')  

* 创建一个项目
* 定义Item容器
* 编写爬虫类
	* 从网页中提取信息（推荐[*beautifulsoup*](https://github.com/ZTCooper/beautifulsoup)）
* 存储数据  

### 一、创建一个项目：  
`> scrapy startproject name`  
  

### 二、定义Item容器：  
（保存爬取到的数据的容器，用法类似dict，提供额外保护机制避免拼写错误导致的未定义字段错误）  
对需要获取的数据进行建模：  
编写**items.py**:  
```Python
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DmozItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()
```
  

### 三、编写爬虫类：  
用于从网上爬取数据的类：  
* 包含用于下载的初始URL
* 如何跟进网页中的连接
* 如何分析页面中的内容
* 提取生成 item 的方法  
  

新建**dmoz_spider.py**：
```Python
import scrapy

class DmozSpider(scrapy.Spider):    #继承于scrapy.Spider
    name = 'dmoz'       #蜘蛛名，必须唯一
    allowed_domains = ['dmoztools.net']     #爬取范围（域名）
    start_urls = [
        'http://dmoztools.net/Computers/Programming/Languages/Python/Books/',
        'http://dmoztools.net/Computers/Programming/Languages/Python/Resources/'
        ]

    def parse(self, response):   #解析response（唯一参数response）
        filename = response.url.split('/')[-2]
        with open(filename, 'wb') as f:
            f.write(response.body)
````
  
运行得到网页源代码  
`> scrapy crawl dmoz`  
  
#### 从网页中提取信息：  
**Scrapy**中使用基于**XPath**和**CSS**的表达机制：**Scrapy Selectors**  
**Selector**是一个选择器，有四个基本方法： 

|方法|说明| 
|----|----|
|**Xpath()**|传入xpath表达式，返回该表达式所对应的所有节点的selector list| 
|**css()**|传入CSS表达式，返回该表达式所对应的所有节点的selector list|
|**extract()**|序列化该节点为unnicode字符串并返回list|
|**re()**|根据传入的正则表达式对数据进行提取，返回unicode字符串list|  
  

     
  
  
启动Scrapy shell:  
```
>scrapy shell "http://dmoztools.net/Computers/Programming/Languages/Python/Books/"  
......  
......  
>>>  
```
使用xpath()：
```
>>> response.xpath('//title')
[<Selector xpath='//title' data='<title>DMOZ - Computers: Programming: La'>]
>>>
>>> response.xpath('//title').extract()
['<title>DMOZ - Computers: Programming: Languages: Python: Books</title>']
>>> # 字符串化
>>>
>>> response.xpath('//title/text()').extract()
['DMOZ - Computers: Programming: Languages: Python: Books']
>>># 去掉标记
>>>
```
......  
......  
......  
  
修改**dmoz_spider.py parse**部分代码：
```Python
import scrapy

class DmozSpider(scrapy.Spider):    #继承于scrapy.Spider
    name = 'dmoz'       #蜘蛛名，必须唯一
    allowed_domains = ['dmoztools.net']     #爬取范围（域名）
    start_urls = [
        'http://dmoztools.net/Computers/Programming/Languages/Python/Books/',
        'http://dmoztools.net/Computers/Programming/Languages/Python/Resources/'
        ]

    def parse(self, response):   #解析response（唯一参数response）
        sites = response.xpath('//div/div')
        for site in sites:
        title = site.xpath('a/div[@class="site-title"]/text()').extract()
        link = site.xpath('a/@href').extract()
        desc = site.xpath('div[@class="site-descr "]/text()').extract()
        print(title, link, desc)
```
  
  
### 四、存储数据：  
在 **dmoz_spider.py** 中导入 **DmozItem**  
`from dmoz.items import DmozItem`  
  
继续修改**dmoz_spider.py**：
```Python
import scrapy

from dmoz.items import DmozItem          #导入 Item

class DmozSpider(scrapy.Spider):         #继承于scrapy.Spider
    name = 'dmoz'                        #蜘蛛名，必须唯一
    allowed_domains = ['dmoztools.net']     #爬取范围（域名）
    start_urls = [
        'http://dmoztools.net/Computers/Programming/Languages/Python/Books/',
        'http://dmoztools.net/Computers/Programming/Languages/Python/Resources/'
        ]

    def parse(self, response):           #解析response（唯一参数response）

        sites = response.xpath('//div/div')
        items = []

        for site in sites:
            item = DmozItem()              #实例化 Item 类为对象赋值 item

            item['title'] = site.xpath('a/div[@class="site-title"]/text()').extract()
            item['link'] = site.xpath('a/@href').extract()
            item['desc'] = site.xpath('div[@class="site-descr "]/text()').extract()
            #类似字典的存储方式

            items.append(item)

        return items
```
  
#### 四种导出形式：json, jsonlines, csv, xml  
`> scrapy crawl dmoz -o items.json -t json`