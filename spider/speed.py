#coding:utf-8
from pyquery import PyQuery as pq
import requests
import json
import os
import urllib
from PIL import Image
import threading
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
    a_list = d('#js_content > table > tbody > tr > td > p > a') + d('#js_content > table > tbody > tr > td  > a')

    url_list = []
    span_list = []

    span_url_dic = {}
    for i, item in enumerate(a_list):
        span_url_dic[item.find('strong').find('span').text if not item.find('strong')is None else
                         item.find('span').find('span').find('strong').text] = item.get('href')
        # span_list.append(item.find('strong').find('span').text if not item.find('strong')is None else
        #                  item.find('span').find('span').find('strong').text)
        # # span_list.append(item.find('strong'))
        #
        # url_list.append(item.get('href'))

    # print(url_list)
    return span_url_dic



# def get_panpan_web():
#     # 防止反爬机制检测 user-agent
#     # header = {
#     #     "token":"76f43218d868401b9204112217b102ee",
#     #
#     # "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)
#     #  Chrome/74.0.3729.169 Safari/537.36",
#     #
#     # }
#
#     resp = requests.get(url)
#     print(type(resp))
#     print(resp.text)

def get_web_info(each_url):
    resp = requests.get(each_url)
    resp.encoding = ('utf-8')
    return resp.text


def spider_info(span_url_dic):
    for k, v in span_url_dic.items():
        # t = threading.Thread(target=execute_begin, args=(k, v,), name="thread-{}".format(k))
        # t.start()
        execute_begin(k, v)


def execute_begin(span_name, each_url):
    html = get_web_info(each_url)
    d = pq(html)
    pic_list = d('#js_content > p > img')
    # 删除开始图片和最后两张图片
    # pic_list.pop(0)
    # pic_list.pop()
    # pic_list.pop()
    img_list = []
    byte_list = []
    for i, item in enumerate(pic_list):
        urllib.request.urlretrieve(item.get("data-src"), '../image/{}{}.png'.format(span_name, i))
        img_list.append('../image/{}{}.png'.format(span_name, i))
    img1 = Image.open(img_list[0])
    img_list.pop(0)
    for t in img_list:
        img = Image.open(t)
        byte_list.append(img)
    img1.save('../query/{}.pdf'.format(span_name), "PDF", resolution=100.0, save_all=True, append_images=byte_list)


def main():
    span_url_dic = get_door_web()
    print(len(span_url_dic))
    spider_info(span_url_dic)
    # resp_list = get_web(url_list)
    # print(resp_list)
    # pq_web(resp)


if __name__ == "__main__":
    main()
