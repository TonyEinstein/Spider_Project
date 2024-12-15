# -*- coding: utf-8 -*-
# @Time    : 2019/6/12 19:00
# @Author  :
# @File    : GetMovie.py

import requests
import logging
import json
from lxml import etree
import pandas as pd

'''
获取数据分析所需的字段内容
抓取字段：影片名，最终评分，五星、四星、三星、二星、一星
抓取的startURL:  
'''

class Movie:

    def __init__(self):
        self.PROXY_POOL_URL = 'http://localhost:5000/get'
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
        # self.proxys = {}

    def get_proxy(self):#代理池 未启用
        try:
            response = requests.get(self.PROXY_POOL_URL)
            if response.status_code == 200:
                return {
                    'http':response.text,
                    'https':response.text
                }
            #proxies=Movie.get_proxy(self)
        except ConnectionError:
            return None


    def getUrl(self,upLimit):
        logging.captureWarnings(True) #关闭多余的警告信息
        for i in range(0, upLimit, 20):
            #确定起始URL
            urls = 'https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=&start={}'.format(i)
            try:
                responses = requests.get(urls,headers=self.headers,timeout=5,verify=False)  # verify=False，不验证证书
                if responses.status_code == 200:
                    #如果起始URL响应正常，打印一下信息
                    print('成功连接： ', urls)
                    responsesDict = json.loads(responses.text)
                    for dicts in responsesDict['data']:
                        url = dicts['url']
                        try:
                            response = requests.get(url, headers=self.headers, timeout=5, verify=False)
                            response.encoding = 'utf-8'
                            if response.status_code == 200: #对是否有正常的响应 加入判断
                                #如果url响应正常打印如下信息
                                print("子网页链接成功： ", url, ' 链接状态 ：', response.status_code, '正在等待解析.....')
                                html = etree.HTML(response.text)
                                #使用xpath进行解析
                                movie_Name_Year = html.xpath('//*[@id="content"]/h1/span/text()')
                                movie_Score = html.xpath(
                                    '//*[@id="interest_sectl"]//div[@class="rating_self clearfix"]/strong/text()')
                                movie_Star = html.xpath(
                                    '//*[@id="interest_sectl"]//div[@class="ratings-on-weight"]/div[@class="item"]/span[@class="rating_per"]/text()')

                                item = [movie_Name_Year[0], movie_Score[0], movie_Star[0], movie_Star[1], movie_Star[2],
                                        movie_Star[3], movie_Star[4]]
                                print('解析成功!')
                                # 名字 电影评分  五星 四星 三星 二星 一星
                                yield item
                            else:
                                pass
                        except:
                            #url没有正常响应
                            print("子网链接失败:  ",url)
                else:
                    pass
            except:
                #起始URL没有返回正常响应
                print('当前urls:  ', urls, '  未响应！')

    def saveFile(self):
        datas = [] #所有数据将加入这里
        for item in Movie.getUrl(self,1200):
            datas.append(item) #添加数据到datas列表
        dataColums = ['影片名', '最终评分', '五星', '四星', '三星', '二星', '一星']
        #将数据转成Dataframe
        files = pd.DataFrame(columns=dataColums, data=datas)
        files.to_csv(r'data.csv',index=None) #=保存到文件
        #成功保存到文件后，打印输出done!提示
        print("done!")

    def main(self):
        Movie.saveFile(self)

if __name__ == '__main__':
    M = Movie()
    M.main()
