#!/usr/bin/env python
# -*- coding: utf-8 -*-
# time: 2024/1/14 18:47
# file: csdn_spider.py
# author: chenruhai
# email: ruhai.chen@qq.com
import concurrent
import sys

import pandas as pd
import requests
from lxml import etree
from tqdm import tqdm
from utils.fake import new_userAgent
from concurrent.futures import ThreadPoolExecutor

def get_URL(URL):
    # header = {"User-Agent":new_userAgent()}
    header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    response = requests.get(url=URL, headers=header)
    # 解码响应对象，得到页面源码
    content = response.text
    # 解析服务器响应的文件
    parse_html = etree.HTML(content)
    urls = parse_html.xpath('//*[@id="articleMeList-blog"]//div[@class="article-item-box csdn-tracking-statistics"]//a/@href')
    return urls

def get_url(url):
    header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    # header = {"User-Agent":new_userAgent()}
    try:
        response = requests.get(url=url, headers=header)
    except Exception as e:
        print(e)
        return "1","1","1","1","1","1",url
    if response.status_code != 200:
        return "0","0","0","0","0","0",url
    # 解码响应对象，得到页面源码
    content = response.text
    # 解析服务器响应的文件
    parse_html = etree.HTML(content)
    # 标题
    title = parse_html.xpath('//*[@id="articleContentId"]/text()')[0].strip().replace("\n", "")
    # 阅读
    read = parse_html.xpath('//*[@id="mainBox"]//div[@class="read-count-box"]/span[@class="read-count"]/text()')[0].replace(" ", "").replace("\n", "")
    # 收藏
    collect = parse_html.xpath('//*[@id="mainBox"]//div[@class="read-count-box"]/a/span[@class="get-collection"]/text()')[0].replace(" ", "").replace("\n", "")
    # 点赞
    like = parse_html.xpath('//*[@id="mainBox"]//div[@class="article-bar-top"]//span[@id="blog-digg-num"]/text()')[0].replace(" ", "").replace("\n", "")
    # 专栏
    special = parse_html.xpath('//*[@id="mainBox"]//div[@class="blog-tags-box"]/div[@class="tags-box artic-tag-box"]//a[@rel="noopener"]/text()')
    special2 = parse_html.xpath('//*[@id="blogColumnPayAdvert"]//div[@class="item-l"]//span[@class="title item-target"]//span[@class="tit"]/text()')

    return title,read,collect,like,special,special2,url

def main():
    # 1.对每一页的文章进行抓取链接
    url_links = []
    for i in tqdm(range(1,10)):
        URL = "https://chenruhai.blog.csdn.net/article/list/{}".format(i)
        try:
            urls = get_URL(URL)
        except Exception as e:
            print(e)
            continue
        print("\n文章列表{}：{}".format(i, urls))
        url_links = url_links + urls
    if url_links==[]:
        print("没有url产出")
        sys.exit()
    # 2.对每篇文章进行抓取内容
    datas = []
    #顺序执行
    # for url in tqdm(url_links):
        # title, limit, read, collect, like, special, url = get_url(url)
        # datas.append([title, limit, read, collect, like, special, url])
    # 执行多线程
    thread_pool = concurrent.futures.ThreadPoolExecutor()
    results = list(tqdm(thread_pool.map(get_url, url_links), desc="并行计算", total=len(url_links), file=sys.stdout,position=0))
    title,read,collect,like,special,special2,url = zip(*results)
    for j in range(len(url)):
        datas.append([title[j],read[j],collect[j],like[j],special[j],special2[j],url[j]])
    thread_pool.shutdown()
    # 存储数据
    df = pd.DataFrame(datas,columns=["标题","阅读","收藏","点赞","分类专栏","专栏","链接"])
    df.to_excel("data3.xlsx",index=False,encoding="utf-8")
    print(df)

if __name__ == '__main__':
    main()