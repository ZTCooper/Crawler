import urllib.request
import os

def url_open(url):
    req = urllib.request.Request(url)         #生成Request对象
    req.add_header('User_Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586')
    response = urllib.request.urlopen(url)
    html = response.read()
    return html
    
def get_page(url):
    html = url_open(url).decode('utf-8')

    a = html.find('current-comment-page') + 23      #+23偏移找到页面数
    b = html.find(']', a)       #从a开始索引

    return html[a:b]
    
def find_imgs(url):
    html = url_open(url).decode('utf-8')
    img_addrs = []
    
    a = html.find('img src=')

    while a != -1:
        b = html.find('.jpg', a, a+225)
        if b != -1:     #找到.jpg
            img_addrs.append(html[a+9:b+4])
        else:
            b = a + 9   #若找不到则向后偏移继续找

        a = html.find('img src=', b)

    return img_addrs


def save_imgs(folder, img_addrs):
    for each in img_addrs:
        filename = each.split('/')[-1]
        with open(filename, 'wb') as f:
            img = url_open('http:'+ each)
            f.write(img)

def download(folder = 'imgs', page=20):     #文件夹名"imgs"，下载前20页
    os.mkdir(folder)
    os.chdir(folder)

    url = 'http://jandan.net/ooxx'
    page_num = int(get_page(url))

    for i in range(page):
        page_num -= i
        page_url = url + '/page-' + str(page_num) + '#comments'
        img_addrs = find_imgs(page_url)
        save_imgs(folder, img_addrs)

if __name__ == '__main__':
    download()
        
    
