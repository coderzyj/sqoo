#coding:utf-8
from pyquery import PyQuery as pq
import requests
import json
import os
import urllib
from PIL import Image
#爬取温州大学首页的报道
#爬取温州大学首页的报道
def getRootPath():
    '''
    获取项目根目录
    :return:
    '''
    rootPath = os.path.dirname(os.path.abspath(__file__))
    return rootPath

rootpath = getRootPath()

url = "https://mp.weixin.qq.com/s/dVSio_SgHfSStP6cWr33uQ"
door_url = "https://mp.weixin.qq.com/s?__biz=Mzg2MjE0Mzc3MA==&mid=100000136&idx=1&sn=e44dd8113ac6634917bab20d2c757002&chksm=4e0d15fd797a9cebece946d5f3911bcb4e1ba223d995640e3e2a8200c9c4c8843fda721b06ec&scene=25#wechat_redirect"

# 获取所有章节
def get_door_web():
    res = requests.get(door_url)
    # print(res.text)
    d = pq(res.text)
    a_list = d('#js_content > table > tbody > tr > td > p > a')
    # a_list = d('#js_content > table')
    url_list = []
    for i, item in enumerate(a_list):
        url_list.append(item.get('href'))
    # print(url_list)
    return url_list



def get_panpan_web():
    # 防止反爬机制检测 user-agent
    # header = {
    #     "token":"76f43218d868401b9204112217b102ee",
    #
    # "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)
    #  Chrome/74.0.3729.169 Safari/537.36",
    #
    # }

    resp = requests.get(url)
    print(type(resp))
    print(resp.text)


def get_web(url_list):
    resp_list = []
    for temp in url_list:
        resp = requests.get(temp)
        resp.encoding = ('utf-8')
        resp_list.append(resp.text)

    print(resp_list)

    return resp_list


def pq_web(html):
    d = pq(html)
    piclist = []
    byte_list = []
    for i in range(7,21):
        title = d('#js_content > p:nth-child({}) > img'.format(i))
        piclist.append(title)
    imgList = []
    for i, item in enumerate(piclist):
        print(item.attr("data-src"), i)
        urllib.request.urlretrieve(item.attr("data-src"), './zhang{}.png'.format(i))
        imgList.append('./zhang{}.png'.format(i))

    img1 = Image.open(imgList[0])
    imgList.pop(0)
    for t in imgList:
        img = Image.open(t)
        byte_list.append(img)
    img1.save('一人之下万人之上.pdf', "PDF", resolution=100.0, save_all=True, append_images=byte_list)
    # filename = rootpath + "\\token.txt"
    # with open(filename, 'w') as f:
    #     f.write(title.attr("data-src"))
    # #print(title.attr("data-src"))
    #
    # with open(filename, 'r') as fd:
    #     line = fd.readline()
    #     print(line)
    #
    # urllib.request.urlretrieve(line, './img1.png')
    # data = requests.get(line)
    # with open(rootpath + "/zhang.jpg", 'w') as t:
    #     t.write(data.content)


def main():
    url_list = get_door_web()
    resp_list = get_web(url_list)
    print(resp_list)
    # pq_web(resp)


if __name__ == "__main__":
    main()
